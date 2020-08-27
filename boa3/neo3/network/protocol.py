import asyncio
import struct
import traceback
import weakref
from asyncio import events
from asyncio.streams import StreamReader, StreamReaderProtocol, StreamWriter
from typing import Optional

from boa3.neo3 import network_logger as logger
from boa3.neo3.core import serialization
from boa3.neo3.network import node
from boa3.neo3.network.message import Message


class NeoProtocol(StreamReaderProtocol):
    def __init__(self, *args, **kwargs):
        """

        Args:
            *args:
            **kwargs:
        """
        sr = StreamReader()
        self._stream_reader_orig = sr
        self._stream_reader_wr = weakref.ref(sr)
        self._stream_writer = None
        self.client = node.NeoNode(self)
        self._loop = events.get_event_loop()
        super().__init__(sr)

    def connection_made(self, transport: asyncio.transports.BaseTransport) -> None:
        super().connection_made(transport)
        self._stream_writer = StreamWriter(transport, self, self._stream_reader_orig, self._loop)

        if self.client:
            asyncio.create_task(self.client.connection_made(transport))

    def connection_lost(self, exc: Optional[Exception] = None) -> None:
        if self.client:
            task = asyncio.create_task(self.client.connection_lost(exc))
            task.add_done_callback(lambda args: super(NeoProtocol, self).connection_lost(exc))
        else:
            super().connection_lost(exc)

    async def send_message(self, message: Message) -> None:
        try:
            self._stream_writer.write(message.to_array())
            await self._stream_writer.drain()
        except ConnectionResetError:
            print("connection reset")
            self.connection_lost(ConnectionResetError())
        except ConnectionError:
            print("connection error")
            self.connection_lost(ConnectionError())
        except asyncio.CancelledError:
            print("task cancelled, closing connection")
            # mypy can't seem to deduce that CancelledError still derives from Exception
            self.connection_lost(asyncio.CancelledError())  # type: ignore
        except Exception as e:
            print(f"***** woah what happened here?! {traceback.format_exc()}")
            self.connection_lost(Exception())

    async def read_message(self, timeout: Optional[int] = 30) -> Optional[Message]:
        if timeout == 0:
            # avoid memleak. See: https://bugs.python.org/issue37042
            timeout = None

        async def _read():
            try:
                # readexactly can throw ConnectionResetError
                message_header = await self._stream_reader_orig.readexactly(3)
                payload_length = message_header[2]

                if payload_length == 0xFD:
                    len_bytes = await self._stream_reader_orig.readexactly(2)
                    payload_length, = struct.unpack("<H", len_bytes)
                elif payload_length == 0xFE:
                    len_bytes = await self._stream_reader_orig.readexactly(4)
                    payload_length, = struct.unpack("<I", len_bytes)
                elif payload_length == 0xFE:
                    len_bytes = await self._stream_reader_orig.readexactly(8)
                    payload_length, = struct.unpack("<Q", len_bytes)
                else:
                    len_bytes = b''

                if payload_length > Message.PAYLOAD_MAX_SIZE:
                    raise ValueError("Invalid format")

                payload_data = await self._stream_reader_orig.readexactly(payload_length)
                raw = message_header + len_bytes + payload_data

                with serialization.BinaryReader(raw) as br:
                    m = Message()
                    try:
                        m.deserialize(br)
                        return m
                    except Exception:
                        logger.debug(f"Failed to deserialize message: {traceback.format_exc()}")
                        return None

            except (ConnectionResetError, ValueError) as e:
                # ensures we break out of the main run() loop of Node, which triggers a disconnect callback to clean up
                self.client.disconnecting = True
                logger.debug(f"Failed to read message data for reason: {traceback.format_exc()}")
                return None
            except (asyncio.CancelledError, asyncio.IncompleteReadError):
                return None
            except Exception:
                # ensures we break out of the main run() loop of Node, which triggers a disconnect callback to clean up
                logger.debug(f"error read message 1 {traceback.format_exc()}")
                return None
        try:
            # logger.debug("trying to read message")
            return await asyncio.wait_for(_read(), timeout)
        except (asyncio.TimeoutError, asyncio.CancelledError):
            return None
        except Exception:
            logger.debug("error read message 2")
            traceback.print_exc()
            return None

    def disconnect(self) -> None:
        if self._stream_writer:
            self._stream_writer.close()
