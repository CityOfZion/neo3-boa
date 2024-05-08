from typing import Self

from boa3.internal import constants
from boa3.internal.neo.contracts import NEF
from boa3.internal.neo.core import BinaryReader, BinaryWriter
from boa3.internal.neo3.contracts.nef import MethodToken


class NefFile:
    """
    The object encapsulates the information of the NEO Executable Format (NEF)

    :ivar _nef: nef serializable object
    """

    def __init__(self, script_bytes: bytes,
                 method_tokens: list[MethodToken] = None,
                 source: str = None):
        """
        :param script_bytes: the script of the smart contract
        """
        compiler: str = f"neo3-boa by COZ-{constants.COMPILER_VERSION}"
        self._nef = NEF(compiler_name=compiler,
                        script=script_bytes,
                        tokens=[] if method_tokens is None else method_tokens,
                        source=source)

    @property
    def script(self) -> bytes:
        return self._nef.script

    @property
    def script_hash(self) -> bytes:
        from boa3.internal.neo.cryptography import hash160
        return hash160(self.script)

    @property
    def source(self) -> str:
        return self._nef.source

    @property
    def checksum(self) -> int:
        return self._nef.checksum

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
    def deserialize(cls, bts: bytes) -> Self:
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
