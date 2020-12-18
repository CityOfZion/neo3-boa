from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MetadataInformationMissing, MismatchedTypes
from boa3.model.builtin.interop.interop import Interop
from boa3.model.type.type import Type
from boa3.neo.core.types.InteropInterface import InteropInterface
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestStorage(BoaTest):

    def test_storage_get_bytes_key(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.StorageGet.storage_context_hash
            + Opcode.SYSCALL
            + Interop.StorageGet.interop_method_hash
            + Opcode.DUP
            + Opcode.ISNULL
            + Opcode.JMPIFNOT
            + Integer(7).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.PUSHDATA1
            + Integer(0).to_byte_array(signed=False, min_length=1)
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/storage_test/StorageGetBytesKey.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('features', manifest)
        self.assertIn('storage', manifest['features'])
        self.assertEqual(True, manifest['features']['storage'])

    def test_storage_get_str_key(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.StorageGet.storage_context_hash
            + Opcode.SYSCALL
            + Interop.StorageGet.interop_method_hash
            + Opcode.DUP
            + Opcode.ISNULL
            + Opcode.JMPIFNOT
            + Integer(7).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.PUSHDATA1
            + Integer(0).to_byte_array(signed=False, min_length=1)
            + Opcode.CONVERT
            + Type.bytes.stack_item
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/storage_test/StorageGetStrKey.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 'example',
                                         expected_result_type=bytes)
        self.assertEqual(b'', result)

        storage = {'example': 23}
        result = self.run_smart_contract(engine, path, 'Main', 'example',
                                         fake_storage=storage,
                                         expected_result_type=bytes)
        self.assertEqual(Integer(23).to_byte_array(), result)

        storage = {'test1': 23, 'test2': 42}
        result = self.run_smart_contract(engine, path, 'Main', 'test2',
                                         fake_storage=storage,
                                         expected_result_type=bytes)
        self.assertEqual(Integer(42).to_byte_array(), result)

    def test_storage_get_mismatched_type(self):
        path = '%s/boa3_test/test_sc/storage_test/StorageGetMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_storage_get_without_metadata(self):
        path = '%s/boa3_test/test_sc/storage_test/StorageGetWithoutMetadata.py' % self.dirname
        self.assertCompilerLogs(MetadataInformationMissing, path)

    def test_storage_get_context(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.StorageGetContext.interop_method_hash
            + Opcode.RET
        )
        path = '%s/boa3_test/test_sc/storage_test/StorageGetContext.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(InteropInterface, result)  # returns an interop interface

    def test_storage_put_bytes_key_bytes_value(self):
        path = '%s/boa3_test/test_sc/storage_test/StoragePutBytesKeyBytesValue.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        stored_value = b'\x01\x02\x03'
        result = self.run_smart_contract(engine, path, 'Main', b'test1')
        self.assertEqual(None, result)
        self.assertTrue(b'test1' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test1'])

        result = self.run_smart_contract(engine, path, 'Main', b'test2')
        self.assertEqual(None, result)
        self.assertTrue(b'test1' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test1'])
        self.assertTrue(b'test2' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test2'])

        result = self.run_smart_contract(engine, path, 'Main', b'test2', fake_storage={})
        self.assertEqual(None, result)
        self.assertTrue(b'test1' not in engine.storage)
        self.assertTrue(b'test2' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test2'])

    def test_storage_put_bytes_key_int_value(self):
        value = Integer(123).to_byte_array()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array(min_length=1, signed=True)
            + value
            + Opcode.CONVERT + Type.int.stack_item
            + Opcode.STLOC0
            + Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array(min_length=1, signed=True)
            + value
            + Opcode.CONVERT + Type.int.stack_item
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.StoragePut.storage_context_hash
            + Opcode.SYSCALL
            + Interop.StoragePut.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/storage_test/StoragePutBytesKeyIntValue.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        stored_value = Integer(123).to_byte_array()
        result = self.run_smart_contract(engine, path, 'Main', b'test1')
        self.assertEqual(None, result)
        self.assertTrue(b'test1' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test1'])

        result = self.run_smart_contract(engine, path, 'Main', b'test2')
        self.assertEqual(None, result)
        self.assertTrue(b'test1' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test1'])
        self.assertTrue(b'test2' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test2'])

        result = self.run_smart_contract(engine, path, 'Main', b'test2', fake_storage={})
        self.assertEqual(None, result)
        self.assertTrue(b'test1' not in engine.storage)
        self.assertTrue(b'test2' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test2'])

    def test_storage_put_bytes_key_str_value(self):
        value = String('123').to_bytes()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array(min_length=1, signed=True)
            + value
            + Opcode.STLOC0
            + Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array(min_length=1, signed=True)
            + value
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.StoragePut.storage_context_hash
            + Opcode.SYSCALL
            + Interop.StoragePut.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/storage_test/StoragePutBytesKeyStrValue.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        stored_value = String('123').to_bytes()
        result = self.run_smart_contract(engine, path, 'Main', 'test1')
        self.assertEqual(None, result)
        self.assertTrue(b'test1' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test1'])

        result = self.run_smart_contract(engine, path, 'Main', 'test2')
        self.assertEqual(None, result)
        self.assertTrue(b'test1' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test1'])
        self.assertTrue(b'test2' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test2'])

        result = self.run_smart_contract(engine, path, 'Main', 'test2', fake_storage={})
        self.assertEqual(None, result)
        self.assertTrue(b'test1' not in engine.storage)
        self.assertTrue(b'test2' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test2'])

    def test_storage_put_str_key_bytes_value(self):
        path = '%s/boa3_test/test_sc/storage_test/StoragePutStrKeyBytesValue.py' % self.dirname
        output = Boa3.compile(path)

        engine = TestEngine(self.dirname)
        stored_value = b'\x01\x02\x03'
        result = self.run_smart_contract(engine, path, 'Main', b'test1')
        self.assertEqual(None, result)
        self.assertTrue(b'test1' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test1'])

        result = self.run_smart_contract(engine, path, 'Main', b'test2')
        self.assertEqual(None, result)
        self.assertTrue(b'test1' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test1'])
        self.assertTrue(b'test2' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test2'])

        result = self.run_smart_contract(engine, path, 'Main', b'test2', fake_storage={})
        self.assertEqual(None, result)
        self.assertTrue(b'test1' not in engine.storage)
        self.assertTrue(b'test2' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test2'])

    def test_storage_put_str_key_int_value(self):
        value = Integer(123).to_byte_array()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array(min_length=1, signed=True)
            + value
            + Opcode.CONVERT + Type.int.stack_item
            + Opcode.STLOC0
            + Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array(min_length=1, signed=True)
            + value
            + Opcode.CONVERT + Type.int.stack_item
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.StoragePut.storage_context_hash
            + Opcode.SYSCALL
            + Interop.StoragePut.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/storage_test/StoragePutStrKeyIntValue.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        stored_value = Integer(123).to_byte_array()
        result = self.run_smart_contract(engine, path, 'Main', 'test1')
        self.assertEqual(None, result)
        self.assertTrue(b'test1' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test1'])

        result = self.run_smart_contract(engine, path, 'Main', 'test2')
        self.assertEqual(None, result)
        self.assertTrue(b'test1' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test1'])
        self.assertTrue(b'test2' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test2'])

        result = self.run_smart_contract(engine, path, 'Main', 'test2', fake_storage={})
        self.assertEqual(None, result)
        self.assertTrue(b'test1' not in engine.storage)
        self.assertTrue(b'test2' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test2'])

    def test_storage_put_str_key_str_value(self):
        value = String('123').to_bytes()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array(min_length=1, signed=True)
            + value
            + Opcode.STLOC0
            + Opcode.PUSHDATA1
            + Integer(len(value)).to_byte_array(min_length=1, signed=True)
            + value
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.StoragePut.storage_context_hash
            + Opcode.SYSCALL
            + Interop.StoragePut.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/storage_test/StoragePutStrKeyStrValue.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        stored_value = String('123').to_bytes()
        result = self.run_smart_contract(engine, path, 'Main', 'test1')
        self.assertEqual(None, result)
        self.assertTrue(b'test1' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test1'])

        result = self.run_smart_contract(engine, path, 'Main', 'test2')
        self.assertEqual(None, result)
        self.assertTrue(b'test1' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test1'])
        self.assertTrue(b'test2' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test2'])

        result = self.run_smart_contract(engine, path, 'Main', 'test2', fake_storage={})
        self.assertEqual(None, result)
        self.assertTrue(b'test1' not in engine.storage)
        self.assertTrue(b'test2' in engine.storage)
        self.assertEqual(stored_value, engine.storage[b'test2'])

    def test_storage_put_mismatched_type_key(self):
        path = '%s/boa3_test/test_sc/storage_test/StoragePutMismatchedTypeKey.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_storage_put_mismatched_type_value(self):
        path = '%s/boa3_test/test_sc/storage_test/StoragePutMismatchedTypeValue.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_storage_delete_bytes_key(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.StorageDelete.storage_context_hash
            + Opcode.SYSCALL
            + Interop.StorageDelete.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/storage_test/StorageDeleteBytesKey.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', b'example')
        self.assertEqual(None, result)
        self.assertFalse(b'example' in engine.storage)

        storage = {'example': 23}
        result = self.run_smart_contract(engine, path, 'Main', b'example', fake_storage=storage)
        self.assertEqual(None, result)
        self.assertTrue('example' in storage)
        self.assertFalse(b'example' in engine.storage)

    def test_storage_delete_str_key(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.StorageDelete.storage_context_hash
            + Opcode.SYSCALL
            + Interop.StorageDelete.interop_method_hash
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/storage_test/StorageDeleteStrKey.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 'example')
        self.assertEqual(None, result)
        self.assertFalse(b'example' in engine.storage)

        storage = {'example': 23}
        result = self.run_smart_contract(engine, path, 'Main', 'example', fake_storage=storage)
        self.assertEqual(None, result)
        self.assertTrue('example' in storage)
        self.assertFalse(b'example' in engine.storage)

    def test_storage_delete_mismatched_type(self):
        path = '%s/boa3_test/test_sc/storage_test/StorageDeleteMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
