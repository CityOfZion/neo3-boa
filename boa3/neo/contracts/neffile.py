from __future__ import annotations

import boa3
from boa3.neo.contracts import NEF, Version
from boa3.neo.core import BinaryReader, BinaryWriter


class NefFile:
    """
    The object encapsulates the information of the NEO Executable Format (NEF)

    :ivar _nef: nef serializable object
    """

    def __init__(self, script_bytes: bytes):
        """
        :param script_bytes: the script of the smart contract
        """
        compiler: str = "neo3-boa by COZ"
        version = Version.from_string(boa3.__version__)
        self._nef = NEF(compiler, version, script_bytes)

    @property
    def script(self) -> bytes:
        return self._nef.script

    @property
    def script_hash(self) -> bytes:
        from boa3.neo.cryptography import hash160
        return hash160(self.script)

    def _set_version(self, version: str):
        """
        Updates the NEF file compiler version
        """
        try:
            version = Version.from_string(version)
            self._nef.version = version
        except Exception as e:
            import logging
            logging.error(str(e))

    def serialize(self) -> bytes:
        """
        Serialize the NefFile object

        :return: bytes of the serialized object.
        """
        with BinaryWriter() as writer:
            self._nef.serialize(writer)
            result = writer.to_array()
        return result

    @classmethod
    def deserialize(cls, bts: bytes) -> NefFile:
        """
        Deserialize the NefFile object

        :param bts: stream data
        :return: the deserialized object.
        :rtype: NefFile
        """
        with BinaryReader(bts) as reader:
            nef = NEF()
            nef.deserialize(reader)

            nef_file = cls(nef.script)
            nef_file._nef = nef
        return nef_file
