from boaconstructor import storage

from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.contracts import FindOptions
from boa3_test.tests import boatestcase


class TestStorageInterop(boatestcase.BoaTestCase):
    from boa3.internal.model.builtin.interop.interop import Interop
    default_folder: str = 'test_sc/interop_test/storage'

    storage_get_context_hash = Interop.StorageGetContext.interop_method_hash
    storage_get_hash = Interop.StorageGet.interop_method_hash
    storage_put_hash = Interop.StoragePut.interop_method_hash
    storage_delete_hash = Interop.StorageDelete.interop_method_hash

    def test_storage_get_bytes_key(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + self.storage_get_context_hash
            + Opcode.SYSCALL
            + self.storage_get_hash
            + Opcode.DUP
            + Opcode.ISNULL
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(signed=True, min_length=1)
            + Opcode.DROP
            + Opcode.PUSHDATA1
            + Integer(0).to_byte_array(signed=False, min_length=1)
            + Opcode.RET
        )

        path = self.get_contract_path('StorageGetBytesKey.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_storage_get_str_key(self):
        path = self.get_contract_path('StorageGetStrKey.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_get_mismatched_type(self):
        path = self.get_contract_path('StorageGetMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    async def test_storage_put_bytes_key_bytes_value(self):
        await self.set_up_contract('StoragePutBytesKeyBytesValue.py')

        storage_key_1 = b'test1'
        storage_key_2 = b'test2'
        stored_value = b'\x01\x02\x03'

        result, _ = await self.call('Main', [storage_key_1], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('Main', [storage_key_2], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('Main', [storage_key_2], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        contract_storage = await self.get_storage()

        self.assertIn(storage_key_1, contract_storage)
        self.assertEqual(stored_value, contract_storage[storage_key_1])

        self.assertIn(storage_key_2, contract_storage)
        self.assertEqual(stored_value, contract_storage[storage_key_2])

    def test_storage_put_bytes_key_int_value_compile(self):
        value = Integer(123).to_byte_array()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.PUSHINT8 + value
            + Opcode.STLOC0
            + Opcode.PUSHINT8 + value
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + self.storage_get_context_hash
            + Opcode.SYSCALL
            + self.storage_put_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StoragePutBytesKeyIntValue.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    async def test_storage_put_bytes_key_int_value(self):
        await self.set_up_contract('StoragePutBytesKeyIntValue.py')

        storage_key_1 = b'test1'
        storage_key_2 = b'test2'
        stored_value = 123

        result, _ = await self.call('Main', [storage_key_1], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('Main', [storage_key_2], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('Main', [storage_key_2], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        contract_storage = await self.get_storage(values_post_processor=storage.as_int)

        self.assertIn(storage_key_1, contract_storage)
        self.assertEqual(stored_value, contract_storage[storage_key_1])

        self.assertIn(storage_key_2, contract_storage)
        self.assertEqual(stored_value, contract_storage[storage_key_2])

    def test_storage_put_bytes_key_str_value_compile(self):
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
            + self.storage_get_context_hash
            + Opcode.SYSCALL
            + self.storage_put_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StoragePutBytesKeyStrValue.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    async def test_storage_put_bytes_key_str_value(self):
        await self.set_up_contract('StoragePutBytesKeyStrValue.py')

        storage_key_1 = b'test1'
        storage_key_2 = b'test2'
        stored_value = '123'

        result, _ = await self.call('Main', [storage_key_1], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('Main', [storage_key_2], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('Main', [storage_key_2], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        contract_storage = await self.get_storage(values_post_processor=storage.as_str)

        self.assertIn(storage_key_1, contract_storage)
        self.assertEqual(stored_value, contract_storage[storage_key_1])

        self.assertIn(storage_key_2, contract_storage)
        self.assertEqual(stored_value, contract_storage[storage_key_2])

    def test_storage_put_str_key_bytes_value(self):
        path = self.get_contract_path('StoragePutStrKeyBytesValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_put_str_key_int_value(self):
        path = self.get_contract_path('StoragePutStrKeyIntValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_put_str_key_str_value(self):
        path = self.get_contract_path('StoragePutStrKeyStrValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_put_mismatched_type_key(self):
        path = self.get_contract_path('StoragePutMismatchedTypeKey.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_put_mismatched_type_value(self):
        path = self.get_contract_path('StoragePutMismatchedTypeValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_delete_bytes_key_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.SYSCALL
            + self.storage_get_context_hash
            + Opcode.SYSCALL
            + self.storage_delete_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StorageDeleteBytesKey.py')
        output = self.compile(path)
        self.assertStartsWith(output, expected_output)

    async def test_storage_delete_bytes_key(self):
        await self.set_up_contract('StorageDeleteBytesKey.py')

        not_existing_key = b'unknown_key'
        storage_key = b'example'

        result, _ = await self.call('has_key', [not_existing_key], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('has_key', [storage_key], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [not_existing_key], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('Main', [storage_key], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('has_key', [storage_key], return_type=bool)
        self.assertEqual(False, result)

        contract_storage = await self.get_storage()

        self.assertNotIn(not_existing_key, contract_storage)
        self.assertNotIn(storage_key, contract_storage)

    def test_storage_delete_str_key(self):
        path = self.get_contract_path('StorageDeleteStrKey.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_delete_mismatched_type(self):
        path = self.get_contract_path('StorageDeleteMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    async def test_storage_find_bytes_prefix(self):
        await self.set_up_contract('StorageFindBytesPrefix.py')

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('find_by_prefix', [b'example'], return_type=list)
            self.assertEqual([], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        contract_storage = await self.get_storage(prefix=b'example')
        self.assertEqual({}, contract_storage)

        example_storage = {
            'example_0': '0',
            'example_1': '1',
            'example_2': '3'
        }
        expected_result = [[key, value] for key, value in example_storage.items()]

        for (key, value) in expected_result:
            await self.call('put_on_storage', [key, value], return_type=None, signing_accounts=[self.genesis])

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('find_by_prefix', [b'example'], return_type=list)
            self.assertEqual(expected_result, result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        contract_storage = await self.get_storage(prefix=b'example', key_post_processor=storage.as_str, values_post_processor=storage.as_str)
        self.assertEqual(example_storage, contract_storage)

    def test_storage_find_str_prefix(self):
        path = self.get_contract_path('StorageFindStrPrefix.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_find_mismatched_type(self):
        path = self.get_contract_path('StorageFindMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_get_context_compile(self):
        expected_output = (
            Opcode.SYSCALL
            + self.storage_get_context_hash
            + Opcode.RET
        )
        path = self.get_contract_path('StorageGetContext.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

    async def test_storage_get_context(self):
        await self.set_up_contract('StorageGetContext.py')

        # StorageContext is an InteropInterface, so it is not possible validate outside of Neo
        with self.assertRaises(ValueError) as context:
            await self.call('main', [], return_type=None)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

    def test_storage_get_read_only_context_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop

        expected_output = (
            Opcode.SYSCALL
            + Interop.StorageGetReadOnlyContext.interop_method_hash
            + Opcode.RET
        )
        path = self.get_contract_path('StorageGetReadOnlyContext.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

    async def test_storage_get_read_only_context(self):
        await self.set_up_contract('StorageGetReadOnlyContext.py')

        # StorageContext is an InteropInterface, so it is not possible validate outside of Neo
        with self.assertRaises(ValueError) as context:
            await self.call('main', [], return_type=None)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

    async def test_storage_get_with_context(self):
        await self.set_up_contract('StorageGetWithContext.py')

        not_existing_key = b'unknown_key'
        result, _ = await self.call('Main', [not_existing_key], return_type=bytes)
        self.assertEqual(b'', result)

        storage_key_1 = b'example'
        storage_key_2 = b'test'
        
        stored_value_1 = Integer(23).to_byte_array()
        stored_value_2 = Integer(42).to_byte_array()
        
        result, _ = await self.call('Main', [storage_key_1], return_type=bytes)
        self.assertEqual(stored_value_1, result)

        result, _ = await self.call('Main', [storage_key_2], return_type=bytes)
        self.assertEqual(stored_value_2, result)

        contract_storage = await self.get_storage()

        self.assertNotIn(not_existing_key, contract_storage)

        self.assertIn(storage_key_1, contract_storage)
        self.assertEqual(stored_value_1, contract_storage[storage_key_1])

        self.assertIn(storage_key_2, contract_storage)
        self.assertEqual(stored_value_2, contract_storage[storage_key_2])

    async def test_storage_put_with_context(self):
        await self.set_up_contract('StoragePutWithContext.py')

        storage_key_1 = b'test1'
        storage_key_2 = b'test2'
        stored_value = b'\x01\x02\x03'

        result, _ = await self.call('Main', [storage_key_1], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('Main', [storage_key_2], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('Main', [storage_key_2], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        contract_storage = await self.get_storage()

        self.assertIn(storage_key_1, contract_storage)
        self.assertEqual(stored_value, contract_storage[storage_key_1])

        self.assertIn(storage_key_2, contract_storage)
        self.assertEqual(stored_value, contract_storage[storage_key_2])

    def test_storage_delete_with_context_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.SYSCALL  # context = get_context()
            + self.storage_get_context_hash
            + Opcode.STLOC0
            + Opcode.LDARG0  # delete(key, context)
            + Opcode.LDLOC0
            + Opcode.SYSCALL
            + self.storage_delete_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StorageDeleteWithContext.py')
        output = self.compile(path)
        self.assertStartsWith(output, expected_output)

    async def test_storage_delete_with_context(self):
        await self.set_up_contract('StorageDeleteWithContext.py')

        not_existing_key = 'unknown_key'
        storage_key = 'example'

        result, _ = await self.call('has_key', [not_existing_key], return_type=bool)
        self.assertEqual(False, result)

        result, _ = await self.call('has_key', [storage_key], return_type=bool)
        self.assertEqual(True, result)

        result, _ = await self.call('Main', [not_existing_key], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('Main', [storage_key], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('has_key', [storage_key], return_type=bool)
        self.assertEqual(False, result)

        contract_storage = await self.get_storage()

        self.assertNotIn(not_existing_key, contract_storage)
        self.assertNotIn(storage_key, contract_storage)

    async def test_storage_find_with_context(self):
        await self.set_up_contract('StorageFindWithContext.py')

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('find_by_prefix', ['example'], return_type=list)
            self.assertEqual([], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        contract_storage = await self.get_storage(prefix=b'example')
        self.assertEqual({}, contract_storage)

        example_storage = {
            'example_0': '0',
            'example_1': '1',
            'example_2': '3'
        }
        expected_result = [[key, value] for key, value in example_storage.items()]

        for (key, value) in expected_result:
            await self.call('put_on_storage', [key, value], return_type=None, signing_accounts=[self.genesis])

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('find_by_prefix', [b'example'], return_type=list)
            self.assertEqual(expected_result, result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        contract_storage = await self.get_storage(prefix=b'example', key_post_processor=storage.as_str, values_post_processor=storage.as_str)
        self.assertEqual(example_storage, contract_storage)

    async def test_storage_find_with_options(self):
        await self.set_up_contract('StorageFindWithOptions.py')

        prefix = 'example'

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('find_by_prefix', [prefix], return_type=list)
            self.assertEqual([], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        contract_storage = await self.get_storage(prefix=b'example')
        self.assertEqual({}, contract_storage)

        expected_result = [['_0', '0'],
                           ['_1', '1'],
                           ['_2', '2']
                           ]
        expected_storage = {item[0]: item[1] for item in expected_result}

        for (key, value) in expected_result:
            await self.call('put_on_storage', [(prefix + key), value], return_type=None, signing_accounts=[self.genesis])

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('find_by_prefix', [prefix], return_type=list)
            self.assertEqual(expected_result, result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        contract_storage = await self.get_storage(prefix=String(prefix).to_bytes(), remove_prefix=True, key_post_processor=storage.as_str, values_post_processor=storage.as_str)
        self.assertEqual(expected_storage, contract_storage)

    async def test_boa2_storage_test(self):
        await self.set_up_contract('StorageBoa2Test.py')

        storage_key = b'something'
        result, _ = await self.call('main', ['sget', storage_key, 'blah'], return_type=bytes)
        self.assertEqual(b'', result)

        result, _ = await self.call('main', ['sput', storage_key, 'blah'], return_type=bool, signing_accounts=[self.genesis])
        self.assertEqual(True, result)

        result, _ = await self.call('main', ['sget', storage_key, 'blah'], return_type=bytes)
        self.assertEqual(b'blah', result)

        result, _ = await self.call('main', ['sdel', storage_key, 'blah'], return_type=bool, signing_accounts=[self.genesis])
        self.assertEqual(True, result)

        result, _ = await self.call('main', ['sget', storage_key, 'blah'], return_type=bytes)
        self.assertEqual(b'', result)

        contract_storage = await self.get_storage()

        self.assertNotIn(storage_key, contract_storage)

    async def test_boa2_storage_test2(self):
        await self.set_up_contract('StorageBoa2Test.py')

        value = 10000000000

        storage_key = Integer(100)
        result, _ = await self.call('main', ['sget', storage_key, value], return_type=bytes)
        self.assertEqual(b'', result)

        result, _ = await self.call('main', ['sput', storage_key, value], return_type=bool, signing_accounts=[self.genesis])
        self.assertEqual(True, result)

        result, _ = await self.call('main', ['sget', storage_key, value], return_type=bytes)
        self.assertEqual(Integer(value).to_byte_array(), result)

        result, _ = await self.call('main', ['sdel', storage_key, value], return_type=bool, signing_accounts=[self.genesis])
        self.assertEqual(True, result)

        result, _ = await self.call('main', ['sget', storage_key, value], return_type=bytes)
        self.assertEqual(b'', result)

        contract_storage = await self.get_storage()

        self.assertNotIn(storage_key.to_byte_array(), contract_storage)

    async def test_storage_between_contracts(self):
        await self.set_up_contract('StorageGetAndPut1.py')
        contract2 = await self.compile_and_deploy('StorageGetAndPut2.py')

        key = b'example_key'
        value = 42

        result, _ = await self.call('put_value', [key, value], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('get_value', [key], return_type=int, target_contract=contract2)
        self.assertEqual(0, result)

        result, _ = await self.call('get_value', [key], return_type=int)
        self.assertEqual(value, result)

        contract1_storage = await self.get_storage(values_post_processor=storage.as_int)
        self.assertIn(key, contract1_storage)
        self.assertEqual(value, contract1_storage[key])

        contract2_storage = await self.get_storage(target_contract=contract2)
        self.assertNotIn(key, contract2_storage)

    async def test_create_map(self):
        await self.set_up_contract('StorageCreateMap.py')

        map_key = b'example_'
        storage_key = b'test1'
        stored_value = b'123'

        result, _ = await self.call('get_from_map', [storage_key], return_type=bytes)
        self.assertEqual(b'', result)

        result, _ = await self.call('insert_to_map', [storage_key, stored_value], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('get_from_map', [b'test1'], return_type=bytes)
        self.assertEqual(stored_value, result)

        contract_storage = await self.get_storage()

        self.assertNotIn(storage_key, contract_storage)

        self.assertIn(map_key + storage_key, contract_storage)
        self.assertEqual(stored_value, contract_storage[map_key + storage_key])

        result, _ = await self.call('delete_from_map', [b'test1'], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('get_from_map', [b'test1'], return_type=bytes)
        self.assertEqual(b'', result)

    async def test_import_storage(self):
        await self.set_up_contract('ImportStorage.py')

        prefix = b'unit'
        key = prefix + b'_test'
        key_str = String.from_bytes(key)
        value = 1234

        result, _ = await self.call('get_value', [key], return_type=int)
        self.assertEqual(0, result)

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('find_by_prefix', [prefix], return_type=list)
            self.assertEqual([], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        contract_storage = await self.get_storage(prefix=prefix)
        self.assertEqual({}, contract_storage)

        result, _ = await self.call('put_value', [key, value], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('get_value', [key], return_type=int)
        self.assertEqual(value, result)

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('find_by_prefix', [prefix], return_type=list)
            self.assertEqual([[key_str, Integer(value).to_byte_array()]], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        contract_storage = await self.get_storage(prefix=prefix, key_post_processor=storage.as_str)
        self.assertEqual({key_str: Integer(value).to_byte_array()}, contract_storage)

        await self.call('put_value', [key, value], return_type=None, signing_accounts=[self.genesis])
        await self.call('get_value', [key], return_type=int)

        result, _ = await self.call('delete_value', [key], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('get_value', [key], return_type=int)
        self.assertEqual(0, result)

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('find_by_prefix', [prefix], return_type=list)
            self.assertEqual([], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        contract_storage = await self.get_storage(prefix=prefix)
        self.assertEqual({}, contract_storage)

    async def test_import_interop_storage(self):
        await self.set_up_contract('ImportInteropStorage.py')

        prefix = b'unit'
        key = prefix + b'_test'
        key_str = String.from_bytes(key)
        value = 1234

        result, _ = await self.call('get_value', [key], return_type=int)
        self.assertEqual(0, result)

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('find_by_prefix', [prefix], return_type=list)
            self.assertEqual([], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        contract_storage = await self.get_storage(prefix=prefix)
        self.assertEqual({}, contract_storage)

        result, _ = await self.call('put_value', [key, value], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('get_value', [key], return_type=int)
        self.assertEqual(value, result)

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('find_by_prefix', [prefix], return_type=list)
            self.assertEqual([[key_str, Integer(value).to_byte_array()]], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        contract_storage = await self.get_storage(prefix=prefix, key_post_processor=storage.as_str)
        self.assertEqual({key_str: Integer(value).to_byte_array()}, contract_storage)

        await self.call('put_value', [key, value], return_type=None, signing_accounts=[self.genesis])
        await self.call('get_value', [key], return_type=int)

        result, _ = await self.call('delete_value', [key], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('get_value', [key], return_type=int)
        self.assertEqual(0, result)

        # TODO: #86drqwhx0 neo-go in the current version of boa-test-constructor is not configured to return Iterators
        with self.assertRaises(ValueError) as context:
            result, _ = await self.call('find_by_prefix', [prefix], return_type=list)
            self.assertEqual([], result)

        self.assertRegex(str(context.exception), 'Interop stack item only supports iterators')

        contract_storage = await self.get_storage(prefix=prefix)
        self.assertEqual({}, contract_storage)

    async def test_as_read_only(self):
        await self.set_up_contract('StorageAsReadOnly.py')

        key = b'key'
        value_old = 'old value'
        value_new = 'new value'

        # Putting old value in the storage
        result, _ = await self.call('put_value_in_storage', [key, value_old], return_type=None, signing_accounts=[self.genesis])
        self.assertEqual(None, result)

        result, _ = await self.call('get_value_in_storage_read_only', [key], return_type=str)
        self.assertEqual(value_old, result)

        result, _ = await self.call('get_value_in_storage', [key], return_type=str)
        self.assertEqual(value_old, result)

        result, _ = await self.call('get_value_in_storage_read_only', [key], return_type=str)
        self.assertEqual(value_old, result)

        result, _ = await self.call('get_value_in_storage', [key], return_type=str)
        self.assertEqual(value_old, result)

        # Trying to put a new value in the storage using read_only won't work
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('put_value_in_storage_read_only', [key, value_new], return_type=None, signing_accounts=[self.genesis])

        self.assertRegex(str(context.exception), 'storage.Context is read only')

    async def test_find_options_values(self):
        await self.set_up_contract('FindOptionsValues.py')

        result, _ = await self.call('main', [FindOptions.KEYS_ONLY], return_type=int)
        self.assertEqual(FindOptions.KEYS_ONLY, result)

        result, _ = await self.call('option_keys_only', [], return_type=int)
        self.assertEqual(FindOptions.KEYS_ONLY, result)

        result, _ = await self.call('option_remove_prefix', [], return_type=int)
        self.assertEqual(FindOptions.REMOVE_PREFIX, result)

        result, _ = await self.call('option_values_only', [], return_type=int)
        self.assertEqual(FindOptions.VALUES_ONLY, result)

        result, _ = await self.call('option_deserialize_values', [], return_type=int)
        self.assertEqual(FindOptions.DESERIALIZE_VALUES, result)

        result, _ = await self.call('option_pick_field_0', [], return_type=int)
        self.assertEqual(FindOptions.PICK_FIELD_0, result)

        result, _ = await self.call('option_pick_field_1', [], return_type=int)
        self.assertEqual(FindOptions.PICK_FIELD_1, result)

        result, _ = await self.call('option_backwards', [], return_type=int)
        self.assertEqual(FindOptions.BACKWARDS, result)

    def test_find_options_mismatched_type(self):
        path = self.get_contract_path('FindOptionsMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
