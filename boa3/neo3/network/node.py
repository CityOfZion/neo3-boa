from __future__ import annotations

import asyncio
import traceback
from contextlib import suppress
from datetime import datetime
from socket import AF_INET as IP4_FAMILY
from typing import Optional, List, Tuple, Dict, Callable, cast

from boa3.neo3 import network_logger as logger, settings, blockchain
from boa3.neo3.core import types, msgrouter
from boa3.neo3.network import encode_base62, message, payloads, capabilities, protocol as protocol
from boa3.neo3.network.convenience import nodeweight
from boa3.neo3.network.ipfilter import ipfilter


class NeoNode:

    #: List[payloads.NetworkAddress]: a list of known network addresses (class attribute).
    addresses = []  # type: List[payloads.NetworkAddress]

    def __init__(self, protocol):
        self.protocol = protocol
        #: payloads.NetworkAddress: Address of the remote endpoint.
        self.address = payloads.NetworkAddress(state=payloads.AddressState.DEAD)
        self.nodeid: int = id(self)  #: int: Unique identifier.
        self.nodeid_human: str = encode_base62(self.nodeid)  #: str: Human readable id.
        self.version = None
        self.tasks = []
        self.nodeweight = nodeweight.NodeWeight(self.nodeid)
        self.best_height: int = 0  #: int: Best block height of node.
        self.best_height_last_update = datetime.utcnow().timestamp()

        self._read_task = None  # type: asyncio.Task
        #: bool: Whether the node is in the process of disconnecting and shutting down its tasks.
        self.disconnecting: bool = False

        #: Dict[message.MessageType, Callable[[message.Message], None]]: A table matching message types to handler
        #: functions.
        self.dispatch_table: Dict[message.MessageType, Callable[[message.Message], None]] = {
            message.MessageType.ADDR: self.handler_addr,
            message.MessageType.BLOCK: self.handler_block,
            message.MessageType.CONSENSUS: self.handler_consensus,
            message.MessageType.INV: self.handler_inv,
            message.MessageType.FILTERADD: self.handler_filteradd,
            message.MessageType.FILTERCLEAR: self.handler_filterclear,
            message.MessageType.FILTERLOAD: self.handler_filterload,
            message.MessageType.GETADDR: self.handler_getaddr,
            message.MessageType.GETBLOCKS: self.handler_getblocks,
            message.MessageType.GETBLOCKDATA: self.handler_getblockdata,
            message.MessageType.GETDATA: self.handler_getdata,
            message.MessageType.GETHEADERS: self.handler_getheaders,
            message.MessageType.HEADERS: self.handler_headers,
            message.MessageType.MEMPOOL: self.handler_mempool,
            message.MessageType.MERKLEBLOCK: self.handler_merkleblock,
            message.MessageType.PING: self.handler_ping,
            message.MessageType.PONG: self.handler_pong,
            message.MessageType.TRANSACTION: self.handler_transaction
        }

    # connection setup and control functions
    async def connection_made(self, transport) -> None:
        """
        Event called by the :meth:`base protocol <asyncio.BaseProtocol.connection_made>`.
        """
        addr_tuple = self.protocol._stream_writer.get_extra_info('peername')
        address = f"{addr_tuple[0]}:{addr_tuple[1]}"

        network_addr = self._find_address_by_host_port(address)
        if network_addr:
            # this scenario occurs when the NodeManager queues seed nodes
            self.address = network_addr
        else:
            self.address.address = address

        if not ipfilter.is_allowed(addr_tuple[0]):
            logger.debug(f"Blocked by ipfilter: {self.address.address}")
            await self.disconnect(payloads.DisconnectReason.IPFILTER_NOT_ALLOWED)
            return

    async def _do_handshake(self) -> Tuple[bool, Optional[payloads.DisconnectReason]]:
        caps: List[capabilities.NodeCapability] = [capabilities.FullNodeCapability(0)]
        # TODO: fix nonce and port if a service is running
        send_version = message.Message(msg_type=message.MessageType.VERSION,
                                       payload=payloads.VersionPayload.create(nonce=123, user_agent="NEO3-PYTHON",
                                                                              capabilities=caps))
        await self.send_message(send_version)

        m = await self.read_message(timeout=3)
        if not m or m.type != message.MessageType.VERSION:
            await self.disconnect(payloads.DisconnectReason.HANDSHAKE_VERSION_ERROR)
            return (False, payloads.DisconnectReason.HANDSHAKE_VERSION_ERROR)

        if not self._validate_version(m.payload):
            await self.disconnect(payloads.DisconnectReason.HANDSHAKE_VERSION_ERROR)
            return (False, payloads.DisconnectReason.HANDSHAKE_VERSION_ERROR)

        m_verack = message.Message(msg_type=message.MessageType.VERACK)
        await self.send_message(m_verack)

        m = await self.read_message(timeout=3)
        if not m or m.type != message.MessageType.VERACK:
            await self.disconnect(payloads.DisconnectReason.HANDSHAKE_VERACK_ERROR)
            return (False, payloads.DisconnectReason.HANDSHAKE_VERACK_ERROR)

        logger.debug(f"Connected to {self.version.user_agent} @ {self.address.address}: {self.best_height}.")
        msgrouter.on_node_connected(self)

        return (True, None)

    async def disconnect(self, reason: payloads.DisconnectReason) -> None:
        """
        Close the connection to remote endpoint.

        Args:
            reason: reason for disconnecting.
        """
        if self.disconnecting:
            return

        self.disconnecting = True

        logger.debug(f"Disconnect called with reason={reason.name}")
        self.address.disconnect_reason = reason
        if reason in [payloads.DisconnectReason.MAX_CONNECTIONS_REACHED,
                      payloads.DisconnectReason.POOR_PERFORMANCE,
                      payloads.DisconnectReason.HANDSHAKE_VERACK_ERROR,
                      payloads.DisconnectReason.HANDSHAKE_VERSION_ERROR,
                      payloads.DisconnectReason.UNKNOWN]:
            self.address.set_state_poor()
        elif reason == payloads.DisconnectReason.IPFILTER_NOT_ALLOWED:
            self.address.set_state_dead()

        for t in self.tasks:
            t.cancel()
            with suppress(asyncio.CancelledError):
                print(f"waiting for task to cancel {t}.")
                await t
                print("done")
        msgrouter.on_node_disconnected(self, reason)
        self.protocol.disconnect()

    async def connection_lost(self, exc) -> None:
        """
        Event called by the :meth:`base protocol <asyncio.BaseProtocol.connection_lost>`.
        """
        logger.debug(f"{datetime.now()} Connection lost {self.address} exception: {exc}")

        if self.address.is_state_connected:
            await self.disconnect(payloads.DisconnectReason.UNKNOWN)

    def _validate_version(self, version) -> bool:
        if version.nonce == self.nodeid:
            logger.debug("Client is self.")
            return False

        if version.magic != settings.network.magic:
            logger.debug(f"Wrong network id {version.magic}.")
            return False

        for c in version.capabilities:
            if isinstance(c, capabilities.ServerCapability):
                addr = self._find_address_by_host_port(self.address.address)

                if addr:
                    addr.set_state_connected()
                    addr.capabilities = version.capabilities
                else:
                    logger.debug(f"Adding address from outside {self.address.address}.")
                    # new connection initiated from outside
                    addr = payloads.address.NetworkAddress(
                        address=self.address.address,
                        capabilities=version.capabilities,
                        state=payloads.address.AddressState.CONNECTED
                    )
                    self.addresses.append(addr)
                break

        for c in version.capabilities:
            if isinstance(c, capabilities.FullNodeCapability):
                # update nodes height indicator
                self.best_height = c.start_height
                self.best_height_last_update = datetime.utcnow().timestamp()
                self.version = version
                return True
        else:
            return False

    def handler_addr(self, msg: message.Message) -> None:
        """
        Handler for a message with the ADDR type.

        Args:
            msg:
        """
        payload = cast(payloads.AddrPayload, msg.payload)
        self.addresses = list(set(self.addresses + payload.addresses))
        msgrouter.on_addr(payload.addresses)

    def handler_block(self, msg: message.Message) -> None:
        """
        Handler for a message with the BLOCK type.

        Args:
            msg:
        """
        msgrouter.on_block(self.nodeid, msg.payload)

    def handler_consensus(self, msg: message.Message) -> None:
        """
        Handler for a message with the CONSENSUS type.

        Args:
            msg:
        """
        pass

    def handler_inv(self, msg: message.Message) -> None:
        """
        Handler for a message with the INV type.

        Args:
            msg:
        """
        payload = cast(payloads.InventoryPayload, msg.payload)
        if payload.type == payloads.InventoryType.BLOCK:
            # neo-cli broadcasts INV messages on a regular interval. We can use those as trigger to request
            # their latest block height
            if len(payload.hashes) > 0:
                if settings.database:
                    height = max(0, blockchain.Blockchain().height)
                else:
                    height = 0
                m = message.Message(msg_type=message.MessageType.PING,
                                    payload=payloads.PingPayload(height=height))
                self._create_task_with_cleanup(self.send_message(m))
        else:
            logger.debug(f"Message with type INV received. No processing for payload type "  # type:ignore
                         f"{payload.type.name} implemented")

    def handler_filteradd(self, msg: message.Message) -> None:
        """
        Handler for a message with the FILTERADD type.

        Args:
            msg:
        """
        pass

    def handler_filterclear(self, msg: message.Message) -> None:
        """
        Handler for a message with the FILTERCLEAR type.

        Args:
            msg:
        """
        pass

    def handler_filterload(self, msg: message.Message) -> None:
        """
        Handler for a message with the FILTERLOAD type.

        Args:
            msg:
        """
        pass

    def handler_getaddr(self, msg: message.Message) -> None:
        """
        Handler for a message with the GETADDR type.

        Args:
            msg:
        """
        addr_list = []
        for address in self.addresses:  # type: payloads.NetworkAddress
            if address.is_state_new or address.is_state_connected:
                addr_list.append(address)
        self._create_task_with_cleanup(self.send_address_list(addr_list))

    def handler_getblocks(self, msg: message.Message) -> None:
        """
        Handler for a message with the GETBLOCKS type.

        Args:
            msg:
        """
        pass

    def handler_getblockdata(self, msg: message.Message) -> None:
        """
        Handler for a message with the GETBLOCKDATA type.

        Args:
            msg:
        """
        pass

    def handler_getdata(self, msg: message.Message) -> None:
        """
        Handler for a message with the GETDATA type.

        Args:
            msg:
        """
        pass

    def handler_getheaders(self, msg: message.Message) -> None:
        """
        Handler for a message with the GETHEADERS type.

        Args:
            msg:
        """
        pass

    def handler_mempool(self, msg: message.Message) -> None:
        """
        Handler for a message with the MEMPOOL type.

        Args:
            msg:
        """
        pass

    def handler_merkleblock(self, msg: message.Message) -> None:
        """
        Handler for a message with the MERKLEBLOCK type.

        Args:
            msg:
        """
        pass

    def handler_headers(self, msg: message.Message) -> None:
        """
        Handler for a message with the HEADERS type.

        Args:
            msg:
        """
        payload = cast(payloads.HeadersPayload, msg.payload)
        if len(payload.headers) > 0:
            msgrouter.on_headers(self.nodeid, payload.headers)

    def handler_ping(self, msg: message.Message) -> None:
        """
        Handler for a message with the PING type.

        Args:
            msg:
        """
        if settings.database:
            height = max(0, blockchain.Blockchain().height)
        else:
            height = 0
        m = message.Message(msg_type=message.MessageType.PONG,
                            payload=payloads.PingPayload(height=height))
        self._create_task_with_cleanup(self.send_message(m))

    def handler_pong(self, msg: message.Message) -> None:
        """
        Handler for a message with the PONG type.

        Args:
            msg:
        """
        payload = cast(payloads.PingPayload, msg.payload)
        logger.debug(f"Updating node {self.nodeid_human} height "
                     f"from {self.best_height} to {payload.current_height}")
        self.best_height = payload.current_height
        self.best_height_last_update = datetime.utcnow().timestamp()

    def handler_transaction(self, msg: message.Message) -> None:
        """
        Handler for a message with the TRANSACTION type.

        Args:
            msg:
        """
        pass

    async def _process_incoming_data(self) -> None:
        """
        Main loop
        """
        logger.debug("Waiting for a message.")
        while not self.disconnecting:
            # we want to always listen for an incoming message
            m = await self.read_message(timeout=1)
            if m is None:
                continue

            handler = self.dispatch_table.get(m.type, None)
            if handler:
                handler(m)
            else:
                logger.debug(f"Unknown message with type: {m.type.name}.")

    # raw network commands
    async def request_address_list(self) -> None:
        """
        Send a request for receiving known network addresses.
        """
        m = message.Message(msg_type=message.MessageType.GETADDR)
        await self.send_message(m)

    async def send_address_list(self, network_addresses: List[payloads.NetworkAddress]) -> None:
        """
        Send network addresses.

        Args:
            network_addresses:
        """
        m = message.Message(msg_type=message.MessageType.ADDR,
                            payload=payloads.AddrPayload(addresses=network_addresses))
        await self.send_message(m)

    async def request_headers(self, hash_start: types.UInt256, count: int = None) -> None:
        """
        Send a request for headers from `hash_start` to `hash_start`+`count`.

        Not specifying a `count` results in requesting at most 2000 headers.

        Args:
            hash_start:
            count:
        """
        m = message.Message(msg_type=message.MessageType.GETHEADERS,
                            payload=payloads.GetBlocksPayload(hash_start, count))
        await self.send_message(m)

    async def send_headers(self, headers: List[payloads.Header]) -> None:
        """
        Send a list of Header objects.

        Args:
            headers:
        """
        if len(headers) > 2000:
            headers = headers[:2000]

        m = message.Message(msg_type=message.MessageType.HEADERS, payload=payloads.HeadersPayload(headers))
        await self.send_message(m)

    async def request_blocks(self, hash_start: types.UInt256, count: int = None) -> None:
        """
        Send a request for retrieving block hashes from `hash_start` to `hash_start`+`count`.

        Not specifying a `count` results in requesting at most 500 blocks.

        Note:
            The remote node is expected to reply with a Message with the :const:`~neo3.network.message.MessageType.INV`
            type containing the hashes of the requested blocks. Use :meth:`~neo3.network.node.NeoNode.request_data` in
            combination with these hashes to return the actual :class:`~neo3.network.payloads.block.Block` objects.

        See also:
            :meth:`~neo3.network.node.NeoNode.request_block_data()` to immediately retrieve
            :class:`~neo3.network.payloads.block.Block` objects.

        Args:
            hash_start:
            count:
        """
        m = message.Message(msg_type=message.MessageType.GETBLOCKS,
                            payload=payloads.GetBlocksPayload(hash_start, count))
        await self.send_message(m)

    async def request_block_data(self, index_start, count) -> None:
        """
        Send a request for `count` blocks starting from `index_start`.

        Count cannot exceed :attr:`~neo3.network.payloads.block.GetBlockDataPayload.MAX_BLOCKS_COUNT`.

        See also:
            :meth:`~neo3.network.node.NeoNode.request_blocks()` to only request block hashes.

        Args:
            index_start: block index to start from.
            count: number of blocks to return.
        """
        m = message.Message(msg_type=message.MessageType.GETBLOCKDATA,
                            payload=payloads.GetBlockDataPayload(index_start, count))
        await self.send_message(m)

    async def request_data(self, type: payloads.InventoryType, hashes: List[types.UInt256]) -> None:
        """
        Send a request for receiving the specified inventory data.

        Args:
            type:
            hashes:
        """
        if len(hashes) < 1:
            return

        m = message.Message(msg_type=message.MessageType.GETDATA, payload=payloads.InventoryPayload(type, hashes))
        await self.send_message(m)

    async def send_inventory(self, inv_type: payloads.InventoryType, inv_hash: types.UInt256):
        inv = payloads.InventoryPayload(type=inv_type, hashes=[inv_hash])
        m = message.Message(msg_type=message.MessageType.INV, payload=inv)
        await self.send_message(m)

    async def relay(self, inventory: payloads.IInventory) -> bool:
        """
        Relay the inventory to the network

        Args:
            inventory: should be of type Block, Transaction or Consensus. See: :class:`~neo3.network.payloads.inventory.InventoryType`. # noqa
        """
        await self.send_inventory(inventory.inventory_type, inventory.hash())
        return True

    # utility functions
    async def send_message(self, message: message.Message) -> None:
        """
        Send a Message over the wire.

        Args:
            message:
        """
        await self.protocol.send_message(message)

    async def read_message(self, timeout: int = 30) -> Optional[message.Message]:
        """
        Read a Message from the wire.

        Args:
            timeout: maximum time to wait in trying to deserialize a message from the wire.

        Returns:
            Message, if enough data was found and successfully deserialized.
            None otherwise.
        """
        return await self.protocol.read_message(timeout)

    def __eq__(self, other):
        if type(other) is type(self):
            return self.address == other.address and self.nodeid == other.nodeid
        else:
            return False

    def __repr__(self):
        return f"<{self.__class__.__name__} at {hex(id(self))}> {self.nodeid_human}"

    @staticmethod
    async def connect_to(host: str = None,
                         port: int = None,
                         timeout=3,
                         loop=None,
                         socket=None) -> Tuple[Optional[NeoNode], Optional[Tuple[str, str]]]:
        """
        Establish a connection to a Neo node

        Note: performs the initial connection handshake and validation.

        Args:
            host: remote address in IPv4 format
            port: remote port
            timeout: maximum time establishing a connection may take
            loop: custom loop

        Raises:
            ValueError: if host/port and the socket argument as specified as the same time or none are specified.

        Returns:
            Tuple:
                - (Node instance, None) - if a connection was successfully established
                - (None, (ip address, error reason)) - if a connection failed to establish . Reasons include connection timeout, connection full and handshake errors. # noqa
        """
        if loop is None:
            loop = asyncio.get_event_loop()

        if host is not None or port is not None:
            if socket is not None:
                raise ValueError('host/port and socket can not be specified at the same time')
        if socket is None and (host is None or port is None):
            raise ValueError('host and port was not specified and no sock specified')

        try:
            if socket:
                logger.debug(f"Trying to connect to socket: {socket}.")
                connect_coro = loop.create_connection(protocol.NeoProtocol, sock=socket)
            else:
                logger.debug(f"Trying to connect to: {host}:{port}.")
                connect_coro = loop.create_connection(protocol.NeoProtocol, host, port, family=IP4_FAMILY)
            transport, node = await asyncio.wait_for(connect_coro, timeout)

            success, fail_reason = await node.client._do_handshake()
            if success:
                return node.client, None
            else:
                raise Exception(fail_reason)
        except asyncio.TimeoutError:
            reason = f"Timed out"
        except OSError as e:
            reason = f"Failed to connect for reason {e}"
        except asyncio.CancelledError:
            reason = "Cancelled"
        except Exception as e:
            reason = traceback.format_exc()
        return None, (f"{host}:{port}", reason)

    @classmethod
    def get_address_new(cls) -> Optional[payloads.NetworkAddress]:
        """
        Utility function to return the first address with the state NEW.
        """
        for addr in cls.addresses:
            if addr.is_state_new:
                return addr
        # explicit return to silence mypy
        return None

    def _find_address_by_host_port(self, host_port) -> Optional[payloads.NetworkAddress]:
        addr = payloads.NetworkAddress(address=host_port)
        try:
            idx = self.addresses.index(addr)
            return self.addresses[idx]
        except ValueError:
            return None

    def _create_task_with_cleanup(self, coro):
        task = asyncio.create_task(coro)
        self.tasks.append(task)
        task.add_done_callback(lambda fut: self.tasks.remove(fut))

    def start_message_handler(self) -> None:
        """
        A convenience function to start a message reading loop and forward the messages to their respective handlers as
        configured in :attr:`~neo3.network.node.NeoNode.dispatch_table`.
        """
        # when we break out of the read/write loops, we should make sure we disconnect
        self._read_task = asyncio.create_task(self._process_incoming_data())
        self._read_task.add_done_callback(lambda _:
                                          asyncio.create_task(self.disconnect(payloads.DisconnectReason.UNKNOWN)))

    @classmethod
    def _reset_for_test(cls) -> None:
        cls.addresses = []
