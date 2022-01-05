from __future__ import annotations

import hashlib
from typing import Tuple

from boa3.neo3.core import Size as s, serialization, types, utils


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

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        version_str = "{0}.{1}.{2}.{3}".format(self.major,
                                               self.minor,
                                               self.build,
                                               self.revision)
        from boa3.neo.vm.type.String import String
        version_bytes = String(version_str).to_bytes() + bytes(s.uint64 * 4 - len(version_str))
        writer.write_bytes(version_bytes)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        version_str = reader.read_bytes(s.uint64 * 4).decode('utf-8')

        import re
        version_str = re.sub(r'\x00+', '', version_str)

        major, minor, build, revision = version_str.split('.')
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
    def __init__(self, compiler_name: str = None, version: Version = None, script: bytes = None):
        self.magic = 0x3346454E
        if compiler_name is None:
            self.compiler = 'unknown'
        else:
            self.compiler = compiler_name[:32]
        self.version = version if version else Version()
        self.script = script if script else b''
        self.checksum = self.compute_checksum()

    def __len__(self):
        return (
            s.uint32  # magic
            + 32  # compiler
            + (s.uint64 * 4)  # version
            + 2  # reserve
            + utils.get_var_size(bytes())  # TODO: method tokens
            + 2  # reserve
            + utils.get_var_size(self.script)
            + s.uint32)  # checksum

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return (self.magic == other.magic
                and self.compiler == other.compiler
                and self.version == other.version
                and self.script == other.script
                and self.checksum == other.checksum)

    @property
    def compiler_with_version(self) -> bytes:
        result = '{0}-'.format(self.compiler).encode('utf-8') + self.version.to_array()
        return result[:64] + bytes(64 - len(result))

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        writer.write_uint32(self.magic)
        writer.write_bytes(self.compiler_with_version)

        writer.write_uint16(0)    # 2 reserved bytes
        writer.write_var_bytes(bytes())   # TODO: method tokens
        writer.write_uint16(0)    # 2 reserved bytes

        writer.write_var_bytes(self.script)
        writer.write_bytes(self.checksum)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        self.magic = reader.read_uint32()
        compiler_with_version = reader.read_bytes(64).decode('utf-8')
        self.compiler, version = compiler_with_version.rsplit('-', maxsplit=1)
        self.version = Version.deserialize_from_bytes(version[:32].encode('utf-8'))

        assert reader.read_uint16() == 0    # 2 reserved bytes
        reader.read_var_int(128)            # TODO: method tokens
        assert reader.read_uint16() == 0    # 2 reserved bytes

        self.script = reader.read_var_bytes()
        self.checksum = reader.read_bytes(4)
        if self.checksum != self.compute_checksum():
            raise ValueError("Deserialization error - invalid checksum")

    def script_to_array(self):
        from boa3.neo3.core.serialization import BinaryWriter
        with BinaryWriter() as bw:
            bw.write_var_bytes(self.script)
            return bw._stream.getvalue()

    def tokens_to_array(self):
        from boa3.neo3.core.serialization import BinaryWriter
        with BinaryWriter() as bw:
            bw.write_var_bytes(bytes())
            return bw._stream.getvalue()

    def compute_checksum(self) -> bytes:
        data = (self.magic.to_bytes(4, 'little')
                + self.compiler_with_version
                + bytes(2)  # reserved bytes
                + self.tokens_to_array()   # TODO: method tokens
                + bytes(2)  # reserved bytes
                + self.script_to_array())

        return hashlib.sha256(hashlib.sha256(data).digest()).digest()[:s.uint32]

    def compute_script_hash(self) -> types.UInt160:
        hash = hashlib.new('ripemd160', hashlib.sha256(self.script).digest()).digest()
        return types.UInt160(data=hash)
