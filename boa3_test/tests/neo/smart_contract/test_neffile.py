from unittest import TestCase

from boa3.constants import ENCODING
from boa3.neo import to_script_hash
from boa3.neo.contracts.neffile import NefFile
from boa3.neo.vm.type.Integer import Integer


class TestNefFile(TestCase):
    test_version = '1.2.3'
    test_version_bytes = (
        Integer(1).to_byte_array(min_length=4)
        + Integer(2).to_byte_array(min_length=4)
        + Integer(3).to_byte_array(min_length=4)
        + Integer(0).to_byte_array(min_length=4)
    )
    test_script = b'\x01\x02\x03'

    def create_test_nef(self, test_script):
        nef = NefFile(test_script)
        nef._set_version(self.test_version)
        return nef

    def test_empty_script(self):
        script = bytes()
        nef = self.create_test_nef(script)
        self.assertEqual(len(nef._nef.script), 0)

    def test_script_hash(self):
        script = self.test_script
        nef = self.create_test_nef(script)
        self.assertEqual(len(nef.script_hash), 20)
        self.assertEqual(nef.script_hash, to_script_hash(script))

    def test_serialize(self):
        script = self.test_script
        nef = self.create_test_nef(script)
        result = nef.serialize()

        self.assertEqual(len(result), len(nef._nef))

        # the first 4 bytes of the header are from nef magic
        # the next 32 bytes of the header are from the compiler id
        start, end = (4, 36)
        self.assertEqual(result[start:end], nef._nef.compiler.encode(ENCODING))

        # the next 16 bytes are from the version, 4 bytes for each field
        start, end = (end, end + 16)
        self.assertEqual(result[start:end], self.test_version_bytes)

        # the next 20 bytes are from the scripthash of the smart contract
        start, end = (end, end + 20)
        self.assertEqual(result[start:end], nef._nef.script_hash.to_array())

        # the next 4 bytes are from the check sum of the nef file
        start, end = (end, end + 4)
        self.assertEqual(result[start:end], nef._nef.checksum)

        # the next byte is from the size of the smart contract
        # and the last bytes are from the script of the smart contract, up to 1MB
        self.assertEqual(result[end], len(nef._nef.script))
        start, end = (end + 1, end + 1 + 1024 ** 2)
        self.assertEqual(result[start:end], nef._nef.script)
