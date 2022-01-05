from boa3.boa3 import Boa3
from boa3.exception import CompilerError
from boa3.model.builtin.interop.interop import Interop
from boa3.model.type.type import Type
from boa3.neo.core.types.InteropInterface import InteropInterface
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestStorageInterop(BoaTest):
    default_folder: str = 'test_sc/interop_test/storage'

    def test_storage_get_bytes_key(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.StorageGetContext.interop_method_hash
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

        path = self.get_contract_path('StorageGetBytesKey.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

    def test_storage_get_str_key(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.StorageGetContext.interop_method_hash
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

        path = self.get_contract_path('StorageGetStrKey.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'example',
                                         expected_result_type=bytes)
        self.assertEqual(b'', result)

        storage = {('example', path): 23}
        result = self.run_smart_contract(engine, path, 'Main', 'example',
                                         fake_storage=storage,
                                         expected_result_type=bytes)
        self.assertEqual(Integer(23).to_byte_array(), result)

        storage = {('test1', path): 23, ('test2', path): 42}
        result = self.run_smart_contract(engine, path, 'Main', 'test2',
                                         fake_storage=storage,
                                         expected_result_type=bytes)
        self.assertEqual(Integer(42).to_byte_array(), result)

    def test_storage_get_mismatched_type(self):
        path = self.get_contract_path('StorageGetMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_put_bytes_key_bytes_value(self):
        path = self.get_contract_path('StoragePutBytesKeyBytesValue.py')

        engine = TestEngine()
        stored_value = b'\x01\x02\x03'
        result = self.run_smart_contract(engine, path, 'Main', b'test1')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', b'test2')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', b'test2', fake_storage={})
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNone(storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

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
            + Interop.StorageGetContext.interop_method_hash
            + Opcode.SYSCALL
            + Interop.StoragePut.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StoragePutBytesKeyIntValue.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        stored_value = Integer(123).to_byte_array()
        result = self.run_smart_contract(engine, path, 'Main', b'test1')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', b'test2')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', b'test2', fake_storage={})
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNone(storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

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
            + Interop.StorageGetContext.interop_method_hash
            + Opcode.SYSCALL
            + Interop.StoragePut.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StoragePutBytesKeyStrValue.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        stored_value = String('123').to_bytes()
        result = self.run_smart_contract(engine, path, 'Main', 'test1')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', 'test2')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', 'test2', fake_storage={})
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNone(storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

    def test_storage_put_str_key_bytes_value(self):
        path = self.get_contract_path('StoragePutStrKeyBytesValue.py')

        engine = TestEngine()
        stored_value = b'\x01\x02\x03'
        result = self.run_smart_contract(engine, path, 'Main', b'test1')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', b'test2')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', b'test2', fake_storage={})
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNone(storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

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
            + Interop.StorageGetContext.interop_method_hash
            + Opcode.SYSCALL
            + Interop.StoragePut.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StoragePutStrKeyIntValue.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        stored_value = Integer(123).to_byte_array()
        result = self.run_smart_contract(engine, path, 'Main', 'test1')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', 'test2')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', 'test2', fake_storage={})
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNone(storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

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
            + Interop.StorageGetContext.interop_method_hash
            + Opcode.SYSCALL
            + Interop.StoragePut.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StoragePutStrKeyStrValue.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        stored_value = String('123').to_bytes()
        result = self.run_smart_contract(engine, path, 'Main', 'test1')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', 'test2')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', 'test2', fake_storage={})
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNone(storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

    def test_storage_put_mismatched_type_key(self):
        path = self.get_contract_path('StoragePutMismatchedTypeKey.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_put_mismatched_type_value(self):
        path = self.get_contract_path('StoragePutMismatchedTypeValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_delete_bytes_key(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.StorageGetContext.interop_method_hash
            + Opcode.SYSCALL
            + Interop.StorageDelete.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StorageDeleteBytesKey.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', b'example')
        self.assertIsVoid(result)
        self.assertIsNone(engine.storage_get(b'example', path))

        storage = {('example', path): 23}
        result = self.run_smart_contract(engine, path, 'Main', b'example', fake_storage=storage)
        self.assertIsVoid(result)
        self.assertIsNone(engine.storage_get('example', path))
        self.assertIsNone(engine.storage_get(b'example', path))

    def test_storage_delete_str_key(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + Interop.StorageGetContext.interop_method_hash
            + Opcode.SYSCALL
            + Interop.StorageDelete.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StorageDeleteStrKey.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'example')
        self.assertIsVoid(result)
        self.assertIsNone(engine.storage_get(b'example', path))

        storage = {('example', path): 23}
        result = self.run_smart_contract(engine, path, 'Main', 'example', fake_storage=storage)
        self.assertIsVoid(result)
        self.assertIsNone(engine.storage_get('example', path))
        self.assertIsNone(engine.storage_get(b'example', path))

    def test_storage_delete_mismatched_type(self):
        path = self.get_contract_path('StorageDeleteMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_find_bytes_prefix(self):
        path = self.get_contract_path('StorageFindBytesPrefix.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'find_by_prefix', b'example')
        self.assertEqual([], result)

        storage = {('example_0', path): '0',
                   ('example_1', path): '1',
                   ('example_2', path): '3'}
        expected_result = [[key, value] for (key, sc), value in storage.items()]

        result = self.run_smart_contract(engine, path, 'find_by_prefix', 'example', fake_storage=storage)
        self.assertEqual(expected_result, result)

    def test_storage_find_str_prefix(self):
        path = self.get_contract_path('StorageFindStrPrefix.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'find_by_prefix', 'example')
        self.assertEqual([], result)

        storage = {('example_0', path): '0',
                   ('example_1', path): '1',
                   ('example_2', path): '3'}
        expected_result = [[key, value] for (key, sc), value in storage.items()]

        result = self.run_smart_contract(engine, path, 'find_by_prefix', 'example', fake_storage=storage)
        self.assertEqual(expected_result, result)

    def test_storage_find_mismatched_type(self):
        path = self.get_contract_path('StorageFindMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_get_context(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.StorageGetContext.interop_method_hash
            + Opcode.RET
        )
        path = self.get_contract_path('StorageGetContext.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(InteropInterface, result)  # returns an interop interface

    def test_storage_get_read_only_context(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.StorageGetReadOnlyContext.interop_method_hash
            + Opcode.RET
        )
        path = self.get_contract_path('StorageGetReadOnlyContext.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(InteropInterface, result)  # returns an interop interface

    def test_storage_get_with_context(self):
        path = self.get_contract_path('StorageGetWithContext.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'example',
                                         expected_result_type=bytes)
        self.assertEqual(b'', result)

        storage = {('example', path): 23}
        result = self.run_smart_contract(engine, path, 'Main', 'example',
                                         fake_storage=storage,
                                         expected_result_type=bytes)
        self.assertEqual(Integer(23).to_byte_array(), result)

        storage = {('test1', path): 23, ('test2', path): 42}
        result = self.run_smart_contract(engine, path, 'Main', 'test2',
                                         fake_storage=storage,
                                         expected_result_type=bytes)
        self.assertEqual(Integer(42).to_byte_array(), result)

    def test_storage_put_with_context(self):
        path = self.get_contract_path('StoragePutWithContext.py')

        engine = TestEngine()
        stored_value = b'\x01\x02\x03'
        result = self.run_smart_contract(engine, path, 'Main', b'test1')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', b'test2')
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'Main', b'test2', fake_storage={})
        self.assertIsVoid(result)
        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNone(storage_value)
        storage_value = engine.storage_get(b'test2', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

    def test_storage_delete_with_context(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.SYSCALL    # context = get_context()
            + Interop.StorageGetContext.interop_method_hash
            + Opcode.STLOC0
            + Opcode.LDARG0     # delete(key, context)
            + Opcode.LDLOC0
            + Opcode.SYSCALL
            + Interop.StorageDelete.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StorageDeleteWithContext.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'example')
        self.assertIsVoid(result)
        self.assertIsNone(engine.storage_get(b'example', path))

        storage = {('example', path): 23}
        result = self.run_smart_contract(engine, path, 'Main', 'example', fake_storage=storage)
        self.assertIsVoid(result)
        self.assertIsNone(engine.storage_get('example', path))
        self.assertIsNone(engine.storage_get(b'example', path))

    def test_storage_find_with_context(self):
        path = self.get_contract_path('StorageFindWithContext.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'find_by_prefix', 'example')
        self.assertEqual([], result)

        storage = {('example_0', path): '0',
                   ('example_1', path): '1',
                   ('example_2', path): '3'}
        expected_result = [[key, value] for (key, sc), value in storage.items()]

        result = self.run_smart_contract(engine, path, 'find_by_prefix', 'example', fake_storage=storage)
        self.assertEqual(expected_result, result)

    def test_storage_find_with_options(self):
        path = self.get_contract_path('StorageFindWithOptions.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'find_by_prefix', 'example')
        self.assertEqual([], result)

        prefix = 'example'
        expected_result = [['_0', '0'],
                           ['_1', '1'],
                           ['_2', '2']
                           ]
        storage = {(prefix + key, path): value for (key, value) in expected_result}

        result = self.run_smart_contract(engine, path, 'find_by_prefix', prefix, fake_storage=storage)
        self.assertEqual(expected_result, result)

    def test_boa2_storage_test(self):
        path = self.get_contract_path('StorageBoa2Test.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 'sget', 'something', 'blah')
        if isinstance(result, str):
            result = String(result).to_bytes()
        self.assertEqual(b'', result)

        result = self.run_smart_contract(engine, path, 'main', 'sput', 'something', 'blah')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', 'sget', 'something', 'blah')
        if isinstance(result, str):
            result = String(result).to_bytes()
        self.assertEqual(b'blah', result)

        result = self.run_smart_contract(engine, path, 'main', 'sdel', 'something', 'blah')
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', 'sget', 'something', 'blah')
        if isinstance(result, str):
            result = String(result).to_bytes()
        self.assertEqual(b'', result)

    def test_boa2_storage_test2(self):
        path = self.get_contract_path('StorageBoa2Test.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 'sget', 100, 10000000000)
        if isinstance(result, str):
            result = String(result).to_bytes()
        self.assertEqual(b'', result)

        result = self.run_smart_contract(engine, path, 'main', 'sput', 100, 10000000000)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', 'sget', 100, 10000000000)
        if isinstance(result, bytes):
            result = Integer.from_bytes(result)
        self.assertEqual(10000000000, result)

        result = self.run_smart_contract(engine, path, 'main', 'sdel', 100, 10000000000)
        self.assertEqual(True, result)

        result = self.run_smart_contract(engine, path, 'main', 'sget', 100, 10000000000)
        if isinstance(result, str):
            result = String(result).to_bytes()
        self.assertEqual(b'', result)

    def test_storage_between_contracts(self):
        path1 = self.get_contract_path('StorageGetAndPut1.py')
        path2 = self.get_contract_path('StorageGetAndPut2.py')

        key = 'example_key'
        value = 42
        engine = TestEngine()

        result = self.run_smart_contract(engine, path1, 'put_value', key, value)
        self.assertIsVoid(result)

        storage_value = engine.storage_get(key, path1)
        self.assertIsNotNone(storage_value)
        self.assertEqual(value, Integer.from_bytes(storage_value))

        result = self.run_smart_contract(engine, path2, 'get_value', key)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path1, 'get_value', key)
        self.assertEqual(value, result)

    def test_create_map(self):
        path = self.get_contract_path('StorageCreateMap.py')

        map_key = b'example_'
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'get_from_map', 'test1',
                                         expected_result_type=bytes)
        self.assertEqual(b'', result)

        stored_value = b'123'
        result = self.run_smart_contract(engine, path, 'insert_to_map', 'test1', stored_value)
        self.assertIsVoid(result)

        storage_value = engine.storage_get(b'test1', path)
        self.assertIsNone(storage_value)
        storage_value = engine.storage_get(map_key + b'test1', path)
        self.assertIsNotNone(storage_value)
        self.assertEqual(stored_value, storage_value)

        result = self.run_smart_contract(engine, path, 'get_from_map', 'test1',
                                         expected_result_type=bytes)
        self.assertEqual(stored_value, result)

        result = self.run_smart_contract(engine, path, 'delete_from_map', 'test1')
        self.assertIsVoid(result)

        result = self.run_smart_contract(engine, path, 'get_from_map', 'test1',
                                         expected_result_type=bytes)
        self.assertEqual(b'', result)

    def test_import_storage(self):
        path = self.get_contract_path('ImportStorage.py')
        engine = TestEngine()

        prefix = 'unit'
        key = f'{prefix}_test'
        value = 1234

        result = self.run_smart_contract(engine, path, 'get_value', key)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'find_by_prefix', prefix)
        self.assertEqual([], result)

        result = self.run_smart_contract(engine, path, 'put_value', key, value)
        self.assertIsVoid(result)

        result = self.run_smart_contract(engine, path, 'get_value', key)
        self.assertEqual(value, result)

        result = self.run_smart_contract(engine, path, 'find_by_prefix', prefix)
        self.assertEqual([[key, Integer(value).to_byte_array()]], result)

        result = self.run_smart_contract(engine, path, 'delete_value', key)
        self.assertIsVoid(result)

        result = self.run_smart_contract(engine, path, 'get_value', key)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'find_by_prefix', 'prefix')
        self.assertEqual([], result)

        result = self.run_smart_contract(engine, path, 'find_by_prefix', prefix)
        self.assertEqual([], result)

    def test_import_interop_storage(self):
        path = self.get_contract_path('ImportInteropStorage.py')
        engine = TestEngine()

        prefix = 'unit'
        key = f'{prefix}_test'
        value = 1234

        result = self.run_smart_contract(engine, path, 'get_value', key)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'find_by_prefix', prefix)
        self.assertEqual([], result)

        result = self.run_smart_contract(engine, path, 'put_value', key, value)
        self.assertIsVoid(result)

        result = self.run_smart_contract(engine, path, 'get_value', key)
        self.assertEqual(value, result)

        result = self.run_smart_contract(engine, path, 'find_by_prefix', prefix)
        self.assertEqual([[key, Integer(value).to_byte_array()]], result)

        result = self.run_smart_contract(engine, path, 'delete_value', key)
        self.assertIsVoid(result)

        result = self.run_smart_contract(engine, path, 'get_value', key)
        self.assertEqual(0, result)

        result = self.run_smart_contract(engine, path, 'find_by_prefix', 'prefix')
        self.assertEqual([], result)

        result = self.run_smart_contract(engine, path, 'find_by_prefix', prefix)
        self.assertEqual([], result)

    def test_as_read_only(self):
        path = self.get_contract_path('StorageAsReadOnly.py')
        engine = TestEngine()

        key = 'key'
        value_old = 'old value'
        value_new = 'new value'

        # Putting old value in the storage
        result = self.run_smart_contract(engine, path, 'put_value_in_storage', key, value_old)
        self.assertIsVoid(result)

        result = self.run_smart_contract(engine, path, 'get_value_in_storage_read_only', key)
        self.assertEqual(value_old, result)

        result = self.run_smart_contract(engine, path, 'get_value_in_storage', key)
        self.assertEqual(value_old, result)

        # Trying to put a new value in the storage using read_only won't work
        with self.assertRaises(TestExecutionException):
            self.run_smart_contract(engine, path, 'put_value_in_storage_read_only', key, value_new)

        result = self.run_smart_contract(engine, path, 'get_value_in_storage_read_only', key)
        self.assertEqual(value_old, result)

        result = self.run_smart_contract(engine, path, 'get_value_in_storage', key)
        self.assertEqual(value_old, result)
