from __future__ import annotations

import asyncio
import traceback
from contextlib import suppress
from datetime import datetime
from typing import Dict

from boa3.neo3 import blockchain, network_logger as logger
from boa3.neo3.core import msgrouter
from boa3.neo3.network import payloads, convenience


class SyncManager(convenience._Singleton):
    #: Maximum number of Blocks to cache in memory. Block persisting empties the cache allowing new blocks to be
    #: requested.
    BLOCK_MAX_CACHE_SIZE = 500
    #: Maximum number of blocks to ask per request. Cannot exceed
    #: :attr:`~neo3.network.payloads.block.GetBlockDataPayload.MAX_BLOCKS_COUNT`.
    BLOCK_NETWORK_REQ_LIMIT = 500
    #: Maximum time in seconds that a node may take to respond to a data request before it is tagged and eventually
    #: replaced.
    BLOCK_REQUEST_TIMEOUT = 5

    # init() is used instead of __init__() due to the Singleton inheritance (read its class documentation)
    def init(self):
        self.nodemgr = convenience.NodeManager()  # singleton
        self.ledger = blockchain.Blockchain()  # singleton
        self.block_cache = []
        self.block_requests = dict()  # type: Dict[int, convenience.RequestInfo]
        self.shutting_down = False

        self._is_persisting_blocks = False
        self._tasks = []
        self._service_task = None

        msgrouter.on_block += self.on_block_received

    async def start(self, timeout=5) -> None:
        """
        Start the block syncing service. Requires a started node manager.

        Args:
            timeout: time in seconds to wait for finding a started node manager.

        Raises:
            Exception: if no started Nodemanager is found within `timeout` seconds.
        """
        async def wait_for_nodemanager():
            logger.debug("Waiting for nodemanager to start")
            while not self.nodemgr.is_running:
                await asyncio.sleep(0.1)

        try:
            await asyncio.wait_for(wait_for_nodemanager(), timeout)
        except asyncio.TimeoutError:
            error_msg = f"Nodemanager failed to start within specified timeout {timeout}"
            logger.debug(error_msg)
            await self.shutdown()
            raise Exception(error_msg)

        logger.debug("Starting services")
        self._service_task = asyncio.create_task(self._run_service())

    async def shutdown(self) -> None:
        """
        Gracefully shutdown the sync manager.

        Stops block persisting and all service tasks.

        Note:
            This dependents on asyncio's Task canceling logic. It waits for all tasks to be cancelled and/or stopped
            before returning.
        """
        logger.debug("Syncmanager shutting down")
        self.shutting_down = True
        self.block_cache = []

        logger.debug("Stopping tasks...")
        if self._service_task:
            self._tasks.append(self._service_task)

        for t in self._tasks:
            t.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)

    def on_block_received(self, from_nodeid, block: payloads.Block) -> int:
        try:
            request_info = self.block_requests.pop(block.index)
        except KeyError:
            # Received a block not asked for. Could be:
            # - a very late reply of a node, for which the block was already received and processed via another node
            # - rogue actors sending data
            return -1

        try:
            flight_info = request_info.flights.pop(from_nodeid)
        except KeyError:
            # received a target block from a node not asked from. We can't be sure this is valid
            # restore the request_info
            self.block_requests[block.index] = request_info
            return -2

        now = datetime.utcnow().timestamp()
        delta_time = now - flight_info.start_time
        speed = (len(block) / 1024) / delta_time  # KB/s

        node = self.nodemgr.get_node_by_nodeid(flight_info.node_id)
        if node:
            node.nodeweight.append_new_speed(speed)

        if not self._is_in_blockcache(block.index) and not self.shutting_down:
            self.block_cache.append(block)

        return 0

    async def _run_service(self) -> None:
        while not self.shutting_down:
            await self._check_timeout()
            await self._sync_blocks()
            if not self._is_persisting_blocks and len(self.block_cache) > 0:
                asyncio.create_task(self.persist_blocks())
            await asyncio.sleep(1)

    async def _check_timeout(self) -> int:
        """
        This function checks if any of the outstanding data requests have exceeded the response time threshold.
        If so then the violating node is tagged. Next, a new node is selected to request the data we have not yet
        received in the hope that this node does perform adequately.
        """
        if len(self.block_requests) == 0:
            # no outstanding data requests
            return -1

        timedout_flights = dict()
        now = datetime.utcnow().timestamp()

        # find outstanding requests that timed out
        for height, request_info in self.block_requests.items():
            flight_info = request_info.most_recent_flight()
            if flight_info and now - flight_info.start_time > self.BLOCK_REQUEST_TIMEOUT:
                timedout_flights[height] = flight_info

        if len(timedout_flights) == 0:
            # no timeouts, every request is still nicely within the threshold
            return -2

        remaining_requests = []
        nodes_to_tag_for_timeout = set()
        best_stored_block_height = self._get_best_stored_block_height()
        for height, flight_info in timedout_flights.items():
            # adding to set to ensure we only tag nodes once per request
            nodes_to_tag_for_timeout.add(flight_info.node_id)

            try:
                request_info = self.block_requests[height]
            except KeyError:
                # TODO: check if still possible. After refactor should not be reachable anymore
                continue

            if flight_info.height <= best_stored_block_height:
                with suppress(KeyError):
                    self.block_requests.pop(height)
                continue

            # tag the node for not delivering data within the set threshold
            request_info.mark_failed_node(flight_info.node_id)
            remaining_requests.append(request_info)

        for node_id in nodes_to_tag_for_timeout:
            # affect node weighting by increasing node timeout count
            self.nodemgr.increase_node_timeout_count(node_id)

        if len(remaining_requests) > 0:
            request_info_first = remaining_requests[0]
            request_info_last = remaining_requests[-1]
            # using the last request_info to find a suitable node, because the last request info is always the
            # highest block to look for
            node = self.nodemgr.get_least_failed_node(request_info_last)
            if node is None:
                # no connected nodes that can satisfy our request.
                # Return and let the node manager first resolve finding nodes
                return -3

            # it is only possible to request block data by height (using the GetBlockData payload) for a consecutive
            # range. One option is to find these ranges and send a request for each range. Another option, which keeps
            # the code much simpler, is to just request the full range (from start to end height) and ignore any gaps
            # in the range that have been filled in the mean time by other nodes that timed out.
            # This leads to minimal (acceptable) additional traffic in certain scenarios.
            for request_info in remaining_requests:
                request_info.add_new_flight(convenience.FlightInfo(node.nodeid, request_info.height))

            count = max(1, request_info_last.height - request_info_first.height)
            logger.debug(f"Block timeout for blocks {request_info_first.height} - {request_info_last.height}. "
                         f"Trying again using next available node {node.nodeid_human}. "
                         f"start={request_info_first.height}, count={count}.")
            await node.request_block_data(index_start=request_info_first.height, count=count)
            node.nodeweight.append_new_request_time()

        return 0

    async def persist_blocks(self) -> None:
        self._is_persisting_blocks = True
        self.block_cache.sort(key=lambda b: b.index)
        try:
            while not self.shutting_down:
                try:
                    block = self.block_cache.pop(0)
                except IndexError:
                    # cache empty
                    break
                await self.ledger.persist(block)
                await asyncio.sleep(0)
        except Exception as e:
            logger.debug(f"Unexpected exception happened while processing the block cache: {traceback.format_exc()}")
        finally:
            self._is_persisting_blocks = False

    async def _sync_blocks(self) -> int:
        # to simplify syncing, don't ask for more data when there are still requests in flight
        if len(self.block_requests) > 0:
            return -1

        block_cache_space = self.BLOCK_MAX_CACHE_SIZE - len(self.block_cache)
        if block_cache_space <= 0:
            return -2

        try:
            best_node_height = max(map(lambda node: node.best_height, self.nodemgr.nodes))
        except ValueError:
            # if the node list is empty max() fails on an empty list
            return -3

        node = self.nodemgr.get_node_with_height(best_node_height)
        # if not node:
        #     # no nodes with our desired height. We'll wait for node manager to resolve this
        #     # or for the nodes to increase their height on the next produced block
        #     return -4

        best_block_height = self._get_best_stored_block_height()
        block_request_limit = min(block_cache_space, self.BLOCK_NETWORK_REQ_LIMIT)

        to_fetch_ctr = 0
        for i in range(1, block_request_limit + 1):
            next_block_height = best_block_height + i

            if next_block_height > best_node_height:
                break

            self._add_block_flight_info(node.nodeid, next_block_height)
            to_fetch_ctr += 1

        if to_fetch_ctr > 0:
            index_start = best_block_height + 1
            logger.debug(f"Asking for blocks {index_start} - {index_start + to_fetch_ctr - 1} from {node.nodeid_human} "
                         f"(blocks in cache: {len(self.block_cache)}).")
            await node.request_block_data(index_start=index_start, count=to_fetch_ctr)

        return 0

    def _get_best_stored_block_height(self) -> int:
        """
        Helper to return the highest block in our possession (either in ledger or in block_cache)
        """
        best_block_cache_height = -1
        self.block_cache.sort(key=lambda b: b.index)
        if len(self.block_cache) > 0:
            best_block_cache_height = self.block_cache[-1].index

        ledger_height = self.ledger.height

        return max(ledger_height, best_block_cache_height)

    def _add_block_flight_info(self, nodeid, height: int) -> None:
        request_info = self.block_requests.get(height, None)

        if request_info is None:
            # no outstanding requests for this particular height, so we create it
            req = convenience.RequestInfo(height)
            req.add_new_flight(convenience.FlightInfo(nodeid, height))
            self.block_requests[height] = req
        else:
            request_info.flights.update({nodeid: convenience.FlightInfo(nodeid, height)})

    def _is_in_blockcache(self, block_height: int) -> bool:
        for b in self.block_cache:
            if b.index == block_height:
                return True
        else:
            return False

    def _run_in_loop(self, coro, interval) -> None:
        """
        Helper function to run a coroutine every `interval` seconds as long as the sync manager is running.

        Stores a task in `_tasks`

        Args:
            coro:
            interval:
        """

        async def _t(coro, interval):
            while not self.shutting_down:
                await coro()
                await asyncio.sleep(interval)

        self._tasks.append(asyncio.create_task(_t(coro, interval)))

    def _reset_for_test(self) -> None:
        self.block_cache = []
        self.block_requests = dict()
        self.shutting_down = False

        self._is_persisting_blocks = False
        self._tasks = []
        self._service_task = None
