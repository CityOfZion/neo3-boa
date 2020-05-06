import sys
from unittest import TestCase

from boa3.neo import to_script_hash
from boa3.neo.smart_contract.neffile import NefFile


class TestNefFile(TestCase):
    test_version = '1.2.3'
    test_version_bytes = b'\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00'
    test_script = b'\x01\x02\x03'

    def create_test_nef(self, test_script):
        nef = NefFile(test_script)
        nef.version = self.test_version
        nef.check_sum = nef.compute_check_sum()
        return nef

    def test_empty_script(self):
        script = bytes()
        nef = self.create_test_nef(script)
        self.assertEqual(len(nef.script), 0)

    def test_script_hash(self):
        script = self.test_script
        nef = self.create_test_nef(script)
        self.assertEqual(len(nef.script_hash), 20)
        self.assertEqual(nef.script_hash, to_script_hash(script))

    def test_serialize(self):
        script = self.test_script
        nef = self.create_test_nef(script)
        result = nef.serialize()

        self.assertEqual(len(result), nef.size)

        # the first 4 bytes of the header are from nef magic
        # the next 32 bytes of the header are from the compiler id
        compiler_header_start = 4
        compiler_header_end = 32 + compiler_header_start

        num_bytes_to_fill = 32 - len(nef.compiler)
        expected_compiler_header = bytearray(nef.compiler, encoding='UTF-8')
        expected_compiler_header.extend(bytes(num_bytes_to_fill))
        self.assertEqual(result[compiler_header_start:compiler_header_end], expected_compiler_header)

        # the next 16 bytes are from the version, 4 bytes for each field
        version_header_start = compiler_header_end
        version_header_end = version_header_start + 16
        self.assertEqual(result[version_header_start:version_header_end], self.test_version_bytes)

        # the next 20 bytes are from the scripthash of the smart contract
        script_hash_header_start = version_header_end
        script_hash_header_end = script_hash_header_start + 20
        self.assertEqual(result[script_hash_header_start:script_hash_header_end], nef.script_hash)

        # the next 4 bytes are from the check sum of the nef file
        check_sum_header_start = script_hash_header_end
        check_sum_header_end = check_sum_header_start + 4

        expected_check_sum = nef.compute_check_sum().to_bytes(4, sys.byteorder)
        self.assertEqual(result[check_sum_header_start:check_sum_header_end], expected_check_sum)

        # the next byte is from the size of the smart contract
        # and the last bytes are from the script of the smart contract, up to 1MB
        script_hash_header_start = check_sum_header_end + 1
        script_hash_header_end = script_hash_header_start + 1024 * 1024
        self.assertEqual(result[check_sum_header_end], len(nef.script))
        self.assertEqual(result[script_hash_header_start:script_hash_header_end], nef.script)
