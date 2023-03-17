from __future__ import annotations

import hashlib
from typing import List, Tuple

from boa3.internal.neo3 import contracts
from boa3.internal.neo3.core import Size as s, serialization, types, utils


class Version(serialization.ISerializable):
    """
    Represents the version number of an assembly
    """

    def __init__(self, major: int = 0, minor: int = 0, build: int = 0, revision: int = 0):
        """
        Args:
            major: non interchangeable assembly.
            minor: significant enhancements with backwards compatibility.
            build: recompilation of the same source with possible other compiler or on other platform.
            revision: fully interchangeable. Can be used for example for security fixes.
        """
        if major < 0 or minor < 0 or build < 0 or revision < 0:
            raise ValueError("Negative version numbers are not allowed")

        if major > 255 or minor > 255 or build > 255 or revision > 255:
            raise ValueError("Version numbers cannot exceed 255")

        self.major = major
        self.minor = minor
        self.build = build
        self.revision = revision

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.major == other.major
                and self.minor == other.minor
                and self.build == other.build
                and self.revision == other.revision)

    def __len__(self):
        return s.uint64 + s.uint64 + s.uint64 + s.uint64

    def __str__(self):
        return "{0}.{1}.{2}.{3}".format(self.major,
                                        self.minor,
                                        self.build,
                                        self.revision)

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        version_str = str(self)
        from boa3.internal.neo.vm.type.String import String
        version_bytes = String(version_str).to_bytes() + bytes(s.uint64 * 4 - len(version_str))
        writer.write_bytes(version_bytes)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        version_str = reader.read_bytes(s.uint64 * 4).decode('utf-8')

        import re
        version_str = re.sub(r'\x00+', '', version_str)

        version_split = version_str.split('.')
        while len(version_split) < 4:
            version_split.append('0')

        major, minor, build, revision = version_split
        self.major = int(major)
        self.minor = int(minor)
        self.build = int(build)
        self.revision = int(revision)

    @classmethod
    def _parse_component(self, c: str) -> Tuple[bool, int]:
        try:
            r = int(c)
        except ValueError:
            return False, -1
        if r < 0:
            return False, -1
        if r > 255:
            return False, -1
        return True, r

    @classmethod
    def from_string(cls, input: str) -> Version:
        """
        Parse an instance out of a string.

        Args:
            input: string representing a version number following the format `Major.Minor[.build[.revision]]`.
            Each version part must fit in the range >= 0 <= 255.

        Raises:
            ValueError: if the input cannot be successfully parsed.
        """
        parts = input.split('.')
        if len(parts) < 2 or len(parts) > 4:
            raise ValueError(f"Cannot parse version from: {input}")

        success, major = Version._parse_component(parts[0])
        if not success:
            raise ValueError(f"Cannot parse major field from: {parts[0]}")
        success, minor = Version._parse_component(parts[1])
        if not success:
            raise ValueError(f"Cannot parse minor field from: {parts[1]}")

        if len(parts) > 2:
            success, build = Version._parse_component(parts[2])
            if not success:
                raise ValueError(f"Cannot parse build field from: {parts[2]}")
        else:
            build = 0

        if len(parts) > 3:
            success, revision = Version._parse_component(parts[3])
            if not success:
                raise ValueError(f"Cannot parse revision field from: {parts[3]}")
        else:
            revision = 0
        return cls(major, minor, build, revision)


class NEF(serialization.ISerializable):
    def __init__(self,
                 compiler_name: str = None,
                 script: bytes = None,
                 tokens: List[MethodToken] = None,
                 source: str = None,
                 _magic: int = 0x3346454E):
        self.magic = _magic
        if compiler_name is None:
            self.compiler = 'unknown'
        else:
            self.compiler = compiler_name[:64]
        self.source = source if source else ""
        self.script = script if script else b''
        self._checksum = 0
        self.tokens = [] if tokens is None else tokens
        # this is intentional, because NEO computes the initial checksum by serializing itself while checksum is 0
        self._checksum = self.compute_checksum()

    def __len__(self):
        return (
            s.uint32  # magic
            + 64  # compiler
            + utils.get_var_size(self.source)
            + 1  # reserved
            + utils.get_var_size(self.tokens)
            + 2  # reserved
            + s.uint32  # checksum
            + utils.get_var_size(self.script)
        )

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.magic == other.magic
                and self.compiler == other.compiler
                and self.source == other.source
                and self.script == other.script
                and self.tokens == other.tokens
                and self.checksum == other.checksum
                )

    @property
    def checksum(self) -> int:
        if self._checksum == 0:
            self._checksum = self.compute_checksum()
        return self._checksum

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        writer.write_uint32(self.magic)
        writer.write_bytes(self.compiler.encode('utf-8').ljust(64, b'\x00'))
        writer.write_var_string(self.source)
        writer.write_bytes(b'\x00')
        writer.write_serializable_list(self.tokens)
        writer.write_bytes(b'\x00\x00')
        writer.write_var_bytes(self.script)
        writer.write_uint32(self._checksum)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        if reader.read_uint32() != self.magic:
            raise ValueError("Deserialization error - Incorrect magic")
        self.compiler = reader.read_bytes(64).decode('utf-8').rstrip(b'\x00'.decode())
        self.source = reader.read_var_string(256)
        if reader.read_uint8() != 0:
            raise ValueError("Reserved bytes must be 0")
        self.tokens = reader.read_serializable_list(MethodToken)
        if reader.read_uint16() != 0:
            raise ValueError("Reserved bytes must be 0")

        self.script = reader.read_var_bytes(max=512 * 1024)
        if len(self.script) == 0:
            raise ValueError("Deserialization error - Script can't be empty")

        checksum = int.from_bytes(reader.read_bytes(4), 'little')
        if checksum != self.compute_checksum():
            raise ValueError("Deserialization error - Invalid checksum")
        else:
            self._checksum = checksum

    def compute_checksum(self) -> int:
        return int.from_bytes(
            hashlib.sha256(hashlib.sha256(self.to_array()[:-4]).digest()).digest()[:s.uint32],
            'little'
        )

    @classmethod
    def _serializable_init(cls):
        c = cls()
        c._checksum = 0
        return c


class MethodToken(serialization.ISerializable):
    def __init__(self,
                 hash: types.UInt160,
                 method: str,
                 parameters_count: int,
                 has_return_value: bool,
                 call_flags: contracts.CallFlags):
        self.hash = hash
        self.method = method
        self.parameters_count = parameters_count
        self.has_return_value = has_return_value
        self.call_flags = call_flags

    def __len__(self):
        return s.uint160 + utils.get_var_size(self.method) + s.uint16 + s.uint8 + s.uint8

    def serialize(self, writer: serialization.BinaryWriter):
        writer.write_serializable(self.hash)
        writer.write_var_string(self.method)
        writer.write_uint16(self.parameters_count)
        writer.write_uint8(self.has_return_value)
        writer.write_uint8(self.call_flags.value)

    def deserialize(self, reader: serialization.BinaryReader):
        self.hash = reader.read_serializable(types.UInt160)
        self.method = reader.read_var_string(32)
        self.parameters_count = reader.read_uint16()
        self.has_return_value = bool(reader.read_uint8())
        self.call_flags = contracts.CallFlags(reader.read_uint8())

    @classmethod
    def _serializable_init(cls):
        return cls(types.UInt160.zero(), "", 0, False, contracts.CallFlags.NONE)
