import re
import sys

import boa3
from boa3 import neo
from boa3.constants import SIZE_OF_INT32, SIZE_OF_INT160, DEFAULT_UINT32
from boa3.neo import cryptography
from boa3.neo.utils.serializer import Serializer
from boa3.neo.vm.type.Integer import Integer


class NefFile:
    """
    The object encapsulates the information of the NEO Executable Format (NEF)

    :ivar compiler: the name of the compiler used to generate the file
    :ivar version: the version of the compiler
    :ivar script_hash: the smart contract hash
    :ivar check_sum: the check sum of the file.
    :ivar script: the script of the smart contract
    """
    # Constants
    __COMPILER_HEADER_SIZE = 32
    __VERSION_NUMBER_OF_FIELDS = 4  # major.minor.patch-release
    __VERSION_HEADER_SIZE = __VERSION_NUMBER_OF_FIELDS * SIZE_OF_INT32

    def __init__(self, script_bytes: bytes):
        """
        :param script_bytes: the script of the smart contract
        """
        self.__magic: int = 0x3346454E              # NEO Executable Format 3 (NEF3)
        self.compiler: str = "neo3-boa by COZ"      # Compiler Name
        self.version: str = boa3.__version__        # Compiler Version
        self.check_sum: int = 0

        self.script: bytes = script_bytes           # Smart Contract Script
        self.script_hash: bytes = neo.to_script_hash(self.script)  # Script Hash
        self.check_sum = self.compute_check_sum()   # Checksum

    @property
    def size(self) -> int:
        """
        Get the size in bytes of the NEF file

        :return: size of NEF File.
        """
        # it is calculated with constants to be compatible with Neo code
        # because Python sizeof differs from C# sizeof
        return (
            SIZE_OF_INT32                       # size of magic
            + NefFile.__COMPILER_HEADER_SIZE    # total size of compiler's name
            + NefFile.__VERSION_HEADER_SIZE     # total size of compiler's version
            + SIZE_OF_INT160                    # size of script hash
            + SIZE_OF_INT32                     # size of check sum
            + len(self.script_len_in_bytes)     # size used to store script size
            + len(self.script)                  # size of smart contract script
        )

    @property
    def script_len_in_bytes(self) -> bytes:
        """
        Get the size of the script in bytes to compute the size of the header

        :return: size of the script in bytes.
        """
        return Integer(len(self.script)).to_byte_array()

    @property
    def __header_size_before_check_sum(self) -> int:
        """
        Get the size of the header of the NEF file before the checksum

        :return: size of header.
        """
        return (
            SIZE_OF_INT32                       # size of magic
            + NefFile.__COMPILER_HEADER_SIZE    # total size of compiler's name
            + NefFile.__VERSION_HEADER_SIZE     # total size of compiler's version
            + SIZE_OF_INT160                    # size of script hash
        )

    @property
    def __version_info(self) -> list:
        """
        Returns the information about the compiler version

        :return: a list of the fields of the version
        """
        version_info = re.split('[.-]', self.version)  # major.minor.patch-release

        for index, field in enumerate(version_info):
            try:
                version_info[index] = int(field)
            except ValueError:
                # in python versions, the release field is a string
                # the nef header needs int values in the version
                version_info[index] = DEFAULT_UINT32

        while len(version_info) < NefFile.__VERSION_NUMBER_OF_FIELDS:
            version_info.append(DEFAULT_UINT32)

        return version_info[0:NefFile.__VERSION_NUMBER_OF_FIELDS]

    def serialize(self) -> bytes:
        """
        Serialize the NefFile object

        :return: bytes of the serialized object.
        """
        nef_serializer = Serializer()

        nef_serializer.write_integer(self.__magic)
        nef_serializer.write_string(self.compiler, NefFile.__COMPILER_HEADER_SIZE)

        for info in self.__version_info:
            nef_serializer.write_integer(info)

        nef_serializer.write_bytes(self.script_hash)
        nef_serializer.write_integer(self.check_sum)
        nef_serializer.write_value(self.script)

        return nef_serializer.result

    def compute_check_sum(self) -> int:
        """
        Computes the checksum of the NEF file

        :return: computed check sum.
        """
        serialized = self.serialize()
        size = self.__header_size_before_check_sum
        check_sum = cryptography.sha256(serialized[0:size])
        return int.from_bytes(check_sum[0:SIZE_OF_INT32], sys.byteorder, signed=False)
