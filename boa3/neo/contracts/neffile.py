import boa3
from boa3.neo.contracts import NEF, Version
from boa3.neo.core import BinaryWriter


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
    def script_hash(self) -> bytes:
        return self._nef.script_hash.to_array()

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
