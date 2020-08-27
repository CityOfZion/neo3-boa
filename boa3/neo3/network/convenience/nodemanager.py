from __future__ import annotations

import asyncio
import ipaddress
from contextlib import suppress
from datetime import datetime
from typing import List, Optional

import aiodns  # type: ignore

from boa3.neo3 import network_logger as logger, settings, blockchain
from boa3.neo3.core import msgrouter
from boa3.neo3.network import node, payloads, convenience, message


def is_ip_address(hostname: str) -> bool:
    host = hostname.split(':')[0]
    try:
        ip = ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


class NodeManager(convenience._Singleton):
    """
    This class is a convenience class that helps establish and maintain a pool of active connections to NEO nodes.

    Attention:
        This class is singleton.
    """
    #: Time interval in seconds for asking nodes for their address list.
    ADDR_QUERY_INTERVAL = 15
    #: Time interval in seconds for calling the height monitoring check.
    MONITOR_HEIGHT_INTERVAL = 30

    #: Maximum time in seconds a node may take to update its best height before being removed for being stuck.
    MAX_HEIGHT_UPDATE_DURATION = 120

    #: Time interval in seconds to check the connection pool for open spots.
    POOL_CHECK_INTERVAL = 10
    #: Maximum number of time the minimum connected client setting may be violated by the open connect checker.
    MAX_NODE_POOL_ERROR = 2
    MAX_NODE_POOL_ERROR_COUNT = 0

    #: Maximum number of times adding a block or header may fail before the node is disconnected.
    MAX_NODE_ERROR_COUNT = 5

    #: Maximum number of times a timeout threshold may be exceeded before the node is disconnected.
    #: Requires calling :meth:`~neo3.network.convenience.nodemanager.NodeManager.increase_node_timeout_count` which is
    #: done automatically by the :class:`~neo3.network.convenience.syncmanager.SyncManager` if used.
    MAX_NODE_TIMEOUT_COUNT = 15

    # init() is used instead of __init__() due to the Singleton inheritance (read its class documentation)
    def init(self):
        #: A list of nodes that we're actively using to request data from
        self.nodes = []  # type: List[node.NeoNode]
        #: A list of host:port addresses that have a task pending to to connect to, but are not fully processed
        self.queued_addresses = []

        self.tasks = []
        #: THe maximum number of clients to have connected at any time.
        self.max_clients = 5
        #: The minimum number clients to always have connected. If this is not met
        #: :attr:`~neo3.network.convenience.nodemanager.MAX_NODE_ERROR_COUNT` times then recovery logic will trigger.
        self.min_clients = 1
        self.shutting_down = False
        self.is_running = False

        msgrouter.on_node_connected += self._handle_node_connected
        msgrouter.on_node_disconnected += self._handle_node_disconnected

        self._test_client_provider = None

    def start(self) -> None:
        """
        Start the node manager services. This does 2 things

        1. Connect to the seed list addresses provided in the configuration
        2. Try to maintain a pool of connected nodes according to the `min/max clients` configuration settings and
           monitor that they don't get stuck.
        """
        def _start_services():
            self.is_running = True
            # 2. connect to addresses
            self._run_in_loop(self._fill_open_connection_spots, interval=self.POOL_CHECK_INTERVAL)

            # 3. keep trying to expand our address list with new addresses
            self._run_in_loop(self._query_addresses, interval=self.ADDR_QUERY_INTERVAL)

            # 4. monitor that connected nodes are not stuck
            self._run_in_loop(self._monitor_node_height, interval=self.MONITOR_HEIGHT_INTERVAL)

        # 1. build an initial address list
        task = asyncio.create_task(self._process_seed_list_addresses())
        task.add_done_callback(lambda fut: _start_services())

    async def shutdown(self) -> None:
        """
        Gracefully shutdown the node manager.

        Disconnects all active nodes and stops service tasks.

        Note:
            This dependents on asyncio's Task canceling logic. It waits for all tasks to be cancelled and/or stopped
            before returning.
        """
        self.shutting_down = True

        # shutdown all running tasks for this class
        # to prevent automatic filling of open spots after disconnecting nodes
        logger.debug("stopping tasks...")
        for t in self.tasks:
            t.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)

        # finally disconnect all existing connections
        # we need to create a new list to loop over, because `disconnect` removes items from self.nodes
        to_disconnect = list(map(lambda n: n, self.nodes))
        disconnect_tasks = []
        logger.debug("disconnecting nodes...")
        for n in to_disconnect:
            disconnect_tasks.append(asyncio.create_task(n.disconnect(payloads.DisconnectReason.SHUTTING_DOWN)))
        await asyncio.gather(*disconnect_tasks, return_exceptions=True)

    """
    Start utility functions
    """

    def get_node_addresses(self) -> List[payloads.NetworkAddress]:
        """
        Return the addresses of connected nodes.
        """
        return list(map(lambda n: n.address, self.nodes))

    def get_node_by_nodeid(self, nodeid: int) -> Optional[node.NeoNode]:
        """
        Return the node instance matching the provided nodeid.
        """
        for n in self.nodes:
            if n.nodeid == nodeid:
                return n
        else:
            return None

    def get_node_with_height(self, height: int) -> Optional[node.NeoNode]:
        """
        Return a node that has a chain height of at least `height`.

        Args:
            height: the minimal block height a node must have.

        Returns:
            None if there are no nodes in the current pool that match the criteria.
            Node instance sorted by weight to avoid hitting the same node every time.
        """
        if len(self.nodes) == 0:
            return None

        weights = list(map(lambda n: n.nodeweight, self.nodes))
        # highest weight is taken first
        weights.sort(reverse=True)

        for weight in weights:
            node = self.get_node_by_nodeid(weight.id)
            if node and height <= node.best_height:
                return node
        else:
            # we could not find a node with the height we're looking for
            return None

    def get_least_failed_node(self, ri: convenience.RequestInfo) -> Optional[node.NeoNode]:
        """
        Return the node with the least fail count for the target item as specified in the RequestInfo.

        Args:
            ri: the info object indicating which header or block we filter on.

        Returns:
            None if there are no connected nodes that can provide the target information as specified in the RequestInfo
            Node instance with the lowest failure count.
        """
        # Find the node with the least failures for the item in RequestInfo

        least_failed_times = 999
        least_failed_node = None
        tried_nodes = []

        for n in self.nodes:  # type: node.NeoNode
            if n.disconnecting:
                continue

            if n.best_height < ri.height:
                continue

            failed_times = ri.failed_nodes.get(n.nodeid, 0)
            if failed_times == 0:
                # return the node we haven't tried this request on before
                return n

            tried_nodes.append(n.nodeid)
            if failed_times < least_failed_times:
                least_failed_times = failed_times
                least_failed_node = n

        return least_failed_node

    def increase_node_error_count(self, nodeid: int) -> None:
        """
        Utility function to increase a node's `error_response_count` param by 1 and disconnect the node if it exceeds
        the threshold set by :attr:`~neo3.network.convenience.nodemanager.MAX_NODE_ERROR_COUNT`.

        Args:
            nodeid (:attr:`~neo3.network.node.NeoNode.nodeid`): the specific node to update.
        """
        node = self.get_node_by_nodeid(nodeid)
        if node:
            node.nodeweight.error_response_count += 1

            if node.nodeweight.error_response_count > self.MAX_NODE_ERROR_COUNT:
                logger.debug(f"Disconnecting node {node.nodeid} Reason: max error count threshold exceeded.")
                asyncio.create_task(node.disconnect(reason=payloads.DisconnectReason.POOR_PERFORMANCE))

    def increase_node_timeout_count(self, nodeid: int) -> None:
        """
        Utility function to increase a node's `timeout_count` param by 1 and disconnect the node if it exceeds the
        threshold set by :attr:`~neo3.network.convenience.nodemanager.MAX_NODE_ERROR_COUNT`.

        Args:
            nodeid (:attr:`~neo3.network.node.NeoNode.nodeid`): the specific node to update.
        """
        node = self.get_node_by_nodeid(nodeid)
        if node:
            node.nodeweight.timeout_count += 1

            if node.nodeweight.timeout_count > self.MAX_NODE_TIMEOUT_COUNT:
                logger.debug(f"Disconnecting node {node.nodeid_human} Reason: max timeout count threshold exceeded.")
                asyncio.create_task(node.disconnect(reason=payloads.DisconnectReason.POOR_PERFORMANCE))

    """
    End utility functions
    """

    """
    Start automatic service methods.

    This section contains the logic for establishing and maintaining node connections
    """

    def _handle_node_connected(self, node: node.NeoNode) -> None:
        """ Handle node connection event."""
        self.nodes.append(node)

        with suppress(ValueError):
            self.queued_addresses.remove(node.address)

    def _handle_node_disconnected(self, node: node.NeoNode, reason: payloads.DisconnectReason) -> None:
        """ Handle node disconnection event."""
        with suppress(ValueError):
            self.nodes.remove(node)

        with suppress(ValueError):
            self.queued_addresses.remove(node.address)

    async def _process_seed_list_addresses(self) -> None:
        """
        Parses addresses from the seed list and store valid addresses
        """
        resolver = aiodns.DNSResolver(loop=asyncio.get_event_loop(), timeout=2)

        async def _process(seed):
            host, port = seed.split(':')
            if not is_ip_address(host):
                try:
                    result = await resolver.query(host, 'A')
                    # x = result[0]
                    host = result[0].host
                except aiodns.error.DNSError as e:
                    logger.debug(f"Skipping {host}, address could not be resolved: {e}.")
            node.NeoNode.addresses.append(payloads.NetworkAddress(address=f"{host}:{port}"))

        tasks = []
        for seed in settings.network.seedlist:
            tasks.append(_process(seed))
        await asyncio.gather(*tasks)

    def _connect_done_cb(self, future) -> None:
        node_instance, failure = future.result()
        # failures here are hard failures from asyncio's loop.create_connection()
        if failure:
            logger.debug(f"Failed to connect to {failure[0]} reason: {failure[1]}.")
            tmp_addr = payloads.NetworkAddress(address=failure[0])

            with suppress(ValueError):
                idx = node.NeoNode.addresses.index(tmp_addr)
                addr = node.NeoNode.addresses[idx]
                addr.set_state_dead()
                self.queued_addresses.remove(tmp_addr)

            msgrouter.on_client_connect_done(None, failure)
        else:
            msgrouter.on_client_connect_done(node_instance, None)
            node_instance.start_message_handler()

        self.tasks.remove(future)

    async def _fill_open_connection_spots(self) -> None:
        open_spots = self.max_clients - (len(self.nodes) + len(self.queued_addresses))

        if open_spots > 0:
            logger.debug(f"Found {open_spots} open pool spots, trying to add nodes...")

            # we sort the addresses such that nodes we recently disconnected from are last in the list
            # this matters in case we had to recycle addresses, meaning addresses with state POOR
            # are now labelled NEW again.
            node.NeoNode.addresses.sort(key=lambda addr: addr.last_connected)

            for _ in range(open_spots):
                # now we ask for the first address with the state NEW
                addr = node.NeoNode.get_address_new()
                if addr:
                    # an address can be queued and its state not yet changed to CONNECTED, so we must make sure we're
                    # not trying to connect to an address that is in an ongoing connection state
                    if addr not in self.queued_addresses:
                        logger.debug(f"Adding {addr} to connection queue.")
                        self.queued_addresses.append(addr)
                        if self._test_client_provider:
                            socket_mock = next(self._test_client_provider())
                            task = asyncio.create_task(node.NeoNode.connect_to(socket=socket_mock))
                        else:
                            task = asyncio.create_task(node.NeoNode.connect_to(addr.ip, addr.port))
                        self.tasks.append(task)
                        task.add_done_callback(self._connect_done_cb)
                else:
                    # oh no, we've exhausted our NEW addresses list
                    if len(self.nodes) >= self.min_clients:
                        logger.debug(f"No addresses available to fill spots. However, minimum clients still satisfied.")
                        break
                    else:
                        if self.MAX_NODE_POOL_ERROR_COUNT != self.MAX_NODE_POOL_ERROR:
                            # give our `_query_addresses` loop a chance to collect new addresses from connected nodes
                            self.MAX_NODE_POOL_ERROR_COUNT += 1
                            logger.debug(f"Increasing pool spot error count to {self.MAX_NODE_POOL_ERROR_COUNT}.")
                            break
                        else:
                            # we have no other option then to retry any address we know
                            logger.debug("Recycling old addresses.")
                            for addr in node.NeoNode.addresses:
                                if addr.is_state_poor:
                                    addr.set_state_new()
                            self.MAX_NODE_POOL_ERROR_COUNT = 0
                            break

    async def _query_addresses(self) -> None:
        """
        Ask for the address list of connected nodes on an interval.
        """
        logger.debug(f"Connected node count {len(self.nodes)}.")
        for node in self.nodes:
            logger.debug(f"Asking node {node.nodeid_human} for its address list")
            task = asyncio.create_task(node.request_address_list())
            self.tasks.append(task)
            task.add_done_callback(lambda fut: self.tasks.remove(fut))

    async def _monitor_node_height(self) -> None:
        now = datetime.utcnow().timestamp()
        for node in self.nodes:
            if now - node.best_height_last_update > self.MAX_HEIGHT_UPDATE_DURATION:
                logger.debug(f"Disconnecting node {node.nodeid} Reason: max height update threshold exceeded.")
                asyncio.create_task(node.disconnect(reason=payloads.DisconnectReason.POOR_PERFORMANCE))
            else:
                logger.debug(f"Asking node {node.nodeid_human} to send us a height update (PING)")
                # Request latest height from node
                if settings.database:
                    height = max(0, blockchain.Blockchain().height)
                else:
                    height = 0
                m = message.Message(msg_type=message.MessageType.PING, payload=payloads.PingPayload(height=height))
                task = asyncio.create_task(node.send_message(m))
                self.tasks.append(task)
                task.add_done_callback(lambda fut: self.tasks.remove(fut))

    def _run_in_loop(self, coro_func, interval) -> None:
        """
        Helper function to run a coroutine every `interval` seconds as long as the node manager is running.

        Stores a task in `tasks`

        Args:
            coro:
            interval:
        """
        async def _t(coro_func, interval):
            while not self.shutting_down:
                await coro_func()
                await asyncio.sleep(interval)

        self.tasks.append(asyncio.create_task(_t(coro_func, interval)))

    """
    End automatic service methods.
    """

    def _reset_for_test(self) -> None:
        self.nodes = []
        self.queued_addresses = []
        self.tasks = []
        self._test_client_provider = None
        self.is_running = False
