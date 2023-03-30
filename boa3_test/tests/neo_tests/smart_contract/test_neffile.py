from unittest import TestCase

from boa3.internal import constants
from boa3.internal.neo import to_script_hash
from boa3.internal.neo.contracts.neffile import NefFile
from boa3.internal.neo.vm.type.Integer import Integer


class TestNefFile(TestCase):
    test_script = b'\x01\x02\x03'

    def create_test_nef(self, test_script) -> NefFile:
        nef = NefFile(test_script)
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
        start, end = (0, 4)

        # the next 64 bytes of the header are from the compiler id + version
        start, end = (end, end + 64)
        compiler = result[start:end].replace(b'\x00', b'')
        self.assertEqual(compiler, nef._nef.compiler.encode(constants.ENCODING))

        # the next 2 bytes are reserved for future changes. Have to be zero
        start, end = (end, end + 2)
        self.assertEqual(bytes(2), result[start: end])

        # the next bytes is the size of the method tokens
        # and the following are the tokens itself
        start, end = (end, end + 1)
        self.assertEqual(bytes(1), result[start: end])

        # the next 2 bytes are reserved for future changes. Have to be zero
        start, end = (end, end + 2)
        self.assertEqual(bytes(2), result[start: end])

        # the next byte is from the size of the smart contract
        # and the last bytes are from the script of the smart contract, up to 1MB
        self.assertEqual(result[end], len(nef._nef.script))
        start, end = (end + 1, end + len(nef._nef.script) + 1)
        self.assertEqual(result[start:end], nef._nef.script)

        # the next 4 bytes are from the check sum of the nef file
        start, end = (end, end + 4)
        self.assertEqual(Integer.from_bytes(result[start:end]), nef._nef.checksum)
