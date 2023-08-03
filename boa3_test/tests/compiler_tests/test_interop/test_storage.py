from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.model.builtin.interop.interop import Interop
from boa3.internal.neo.core.types.InteropInterface import InteropInterface
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.contracts import FindOptions
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


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

    def test_storage_put_bytes_key_bytes_value(self):
        path, _ = self.get_deploy_file_paths('StoragePutBytesKeyBytesValue.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        storage_key_1 = b'test1'
        storage_key_2 = b'test2'
        stored_value = b'\x01\x02\x03'

        invokes.append(runner.call_contract(path, 'Main', storage_key_1))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'Main', storage_key_2))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'Main', storage_key_2))
        expected_results.append(None)

        storage_contract = invokes[0].invoke.contract
        runner.execute(get_storage_from=storage_contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        storage_result_1 = runner.storages.get(storage_contract, storage_key_1)
        self.assertEqual(stored_value, storage_result_1.as_bytes())

        storage_result_2 = runner.storages.get(storage_contract, storage_key_2)
        self.assertEqual(stored_value, storage_result_2.as_bytes())

    def test_storage_put_bytes_key_int_value(self):
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
            + Interop.StorageGetContext.interop_method_hash
            + Opcode.SYSCALL
            + Interop.StoragePut.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StoragePutBytesKeyIntValue.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        storage_key_1 = b'test1'
        storage_key_2 = b'test2'
        stored_value = 123

        invokes.append(runner.call_contract(path, 'Main', storage_key_1))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'Main', storage_key_2))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'Main', storage_key_2))
        expected_results.append(None)

        storage_contract = invokes[0].invoke.contract
        runner.execute(get_storage_from=storage_contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        storage_result_1 = runner.storages.get(storage_contract, storage_key_1)
        self.assertEqual(stored_value, storage_result_1.as_int())

        storage_result_2 = runner.storages.get(storage_contract, storage_key_2)
        self.assertEqual(stored_value, storage_result_2.as_int())

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
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        storage_key_1 = b'test1'
        storage_key_2 = b'test2'
        stored_value = '123'

        invokes.append(runner.call_contract(path, 'Main', storage_key_1))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'Main', storage_key_2))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'Main', storage_key_2))
        expected_results.append(None)

        storage_contract = invokes[0].invoke.contract
        runner.execute(get_storage_from=storage_contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        storage_result_1 = runner.storages.get(storage_contract, storage_key_1)
        self.assertEqual(stored_value, storage_result_1.as_str())

        storage_result_2 = runner.storages.get(storage_contract, storage_key_2)
        self.assertEqual(stored_value, storage_result_2.as_str())

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
        output = self.compile(path)
        self.assertStartsWith(output, expected_output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        not_existing_key = b'unknown_key'
        storage_key = b'example'

        invokes.append(runner.call_contract(path, 'has_key', not_existing_key))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'has_key', storage_key))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'Main', not_existing_key))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'Main', storage_key))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'has_key', storage_key))
        expected_results.append(False)

        storage_contract = invokes[0].invoke.contract
        runner.execute(get_storage_from=storage_contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        self.assertIsNone(runner.storages.get(storage_contract, not_existing_key))
        self.assertIsNone(runner.storages.get(storage_contract, storage_key))

    def test_storage_delete_str_key(self):
        path = self.get_contract_path('StorageDeleteStrKey.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_delete_mismatched_type(self):
        path = self.get_contract_path('StorageDeleteMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_storage_find_bytes_prefix(self):
        path, _ = self.get_deploy_file_paths('StorageFindBytesPrefix.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'find_by_prefix', b'example'))
        expected_results.append([])

        runner.execute()  # getting result of multiple iterators is failing
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        storage = {'example_0': '0',
                   'example_1': '1',
                   'example_2': '3'}
        expected_result = [[key, value] for key, value in storage.items()]

        for (key, value) in expected_result:
            runner.call_contract(path, 'put_on_storage', key, value)

        invokes.append(runner.call_contract(path, 'find_by_prefix', b'example'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_storage_find_str_prefix(self):
        path = self.get_contract_path('StorageFindStrPrefix.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(InteropInterface)  # returns an interop interface

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_storage_get_read_only_context(self):
        expected_output = (
            Opcode.SYSCALL
            + Interop.StorageGetReadOnlyContext.interop_method_hash
            + Opcode.RET
        )
        path = self.get_contract_path('StorageGetReadOnlyContext.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(InteropInterface)  # returns an interop interface

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_storage_get_with_context(self):
        path, _ = self.get_deploy_file_paths('StorageGetWithContext.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        not_existing_key = 'unknown_key'
        invokes.append(runner.call_contract(path, 'Main', not_existing_key,
                                            expected_result_type=bytes))
        expected_results.append(b'')

        storage_key_1 = 'example'
        storage_key_2 = 'test'
        invokes.append(runner.call_contract(path, 'Main', storage_key_1,
                                            expected_result_type=bytes))
        expected_results.append(Integer(23).to_byte_array())

        invokes.append(runner.call_contract(path, 'Main', storage_key_2,
                                            expected_result_type=bytes))
        expected_results.append(Integer(42).to_byte_array())

        storage_contract = invokes[0].invoke.contract
        runner.execute(get_storage_from=storage_contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        self.assertIsNone(runner.storages.get(storage_contract, not_existing_key))

        storage_result_1 = runner.storages.get(storage_contract, storage_key_1)
        self.assertEqual(expected_results[1], storage_result_1.as_bytes())

        storage_result_2 = runner.storages.get(storage_contract, storage_key_2)
        self.assertEqual(expected_results[2], storage_result_2.as_bytes())

    def test_storage_put_with_context(self):
        path, _ = self.get_deploy_file_paths('StoragePutWithContext.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        storage_key_1 = 'test1'
        storage_key_2 = 'test2'
        stored_value = b'\x01\x02\x03'

        invokes.append(runner.call_contract(path, 'Main', storage_key_1))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'Main', storage_key_2))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'Main', storage_key_2))
        expected_results.append(None)

        storage_contract = invokes[0].invoke.contract
        runner.execute(get_storage_from=storage_contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        storage_result_1 = runner.storages.get(storage_contract, storage_key_1)
        self.assertEqual(stored_value, storage_result_1.as_bytes())

        storage_result_2 = runner.storages.get(storage_contract, storage_key_2)
        self.assertEqual(stored_value, storage_result_2.as_bytes())

    def test_storage_delete_with_context(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.SYSCALL  # context = get_context()
            + Interop.StorageGetContext.interop_method_hash
            + Opcode.STLOC0
            + Opcode.LDARG0  # delete(key, context)
            + Opcode.LDLOC0
            + Opcode.SYSCALL
            + Interop.StorageDelete.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('StorageDeleteWithContext.py')
        output = self.compile(path)
        self.assertStartsWith(output, expected_output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        not_existing_key = 'unknown_key'
        storage_key = 'example'

        invokes.append(runner.call_contract(path, 'has_key', not_existing_key))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'has_key', storage_key))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'Main', not_existing_key))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'Main', storage_key))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'has_key', storage_key))
        expected_results.append(False)

        storage_contract = invokes[0].invoke.contract
        runner.execute(get_storage_from=storage_contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        self.assertIsNone(runner.storages.get(storage_contract, not_existing_key))
        self.assertIsNone(runner.storages.get(storage_contract, storage_key))

    def test_storage_find_with_context(self):
        path, _ = self.get_deploy_file_paths('StorageFindWithContext.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'find_by_prefix', 'example'))
        expected_results.append([])

        runner.execute()  # getting result of multiple iterators is failing
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        storage = {'example_0': '0',
                   'example_1': '1',
                   'example_2': '3'}
        expected_result = [[key, value] for key, value in storage.items()]

        for (key, value) in expected_result:
            runner.call_contract(path, 'put_on_storage', key, value)

        invokes.append(runner.call_contract(path, 'find_by_prefix', b'example'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_storage_find_with_options(self):
        path, _ = self.get_deploy_file_paths('StorageFindWithOptions.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'find_by_prefix', 'example'))
        expected_results.append([])

        runner.execute()  # getting result of multiple iterators is failing
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        prefix = 'example'
        expected_result = [['_0', '0'],
                           ['_1', '1'],
                           ['_2', '2']
                           ]

        for (key, value) in expected_result:
            runner.call_contract(path, 'put_on_storage', (prefix + key), value)

        invokes.append(runner.call_contract(path, 'find_by_prefix', 'example'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_storage_test(self):
        path, _ = self.get_deploy_file_paths('StorageBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        storage_key = b'something'
        invokes.append(runner.call_contract(path, 'main', 'sget', storage_key, 'blah',
                                            expected_result_type=bytes))
        expected_results.append(b'')

        invokes.append(runner.call_contract(path, 'main', 'sput', storage_key, 'blah'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', 'sget', storage_key, 'blah',
                                            expected_result_type=bytes))
        expected_results.append(b'blah')

        invokes.append(runner.call_contract(path, 'main', 'sdel', storage_key, 'blah'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', 'sget', storage_key, 'blah',
                                            expected_result_type=bytes))
        expected_results.append(b'')

        storage_contract = invokes[0].invoke.contract
        runner.execute(get_storage_from=storage_contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        self.assertIsNone(runner.storages.get(storage_contract, storage_key))

    def test_boa2_storage_test2(self):
        path, _ = self.get_deploy_file_paths('StorageBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        storage_key = Integer(100)
        invokes.append(runner.call_contract(path, 'main', 'sget', storage_key, 10000000000,
                                            expected_result_type=bytes))
        expected_results.append(b'')

        invokes.append(runner.call_contract(path, 'main', 'sput', storage_key, 10000000000))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', 'sget', storage_key, 10000000000,
                                            expected_result_type=int))
        expected_results.append(10000000000)

        invokes.append(runner.call_contract(path, 'main', 'sdel', storage_key, 10000000000))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'main', 'sget', storage_key, 10000000000,
                                            expected_result_type=bytes))
        expected_results.append(b'')

        storage_contract = invokes[0].invoke.contract
        runner.execute(get_storage_from=storage_contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        self.assertIsNone(runner.storages.get(storage_contract, storage_key.to_byte_array()))

    def test_storage_between_contracts(self):
        path1, _ = self.get_deploy_file_paths('StorageGetAndPut1.py')
        path2, _ = self.get_deploy_file_paths('StorageGetAndPut2.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        key = b'example_key'
        value = 42

        invokes.append(runner.call_contract(path1, 'put_value', key, value))
        expected_results.append(None)
        contract_1 = invokes[-1].invoke.contract

        invokes.append(runner.call_contract(path2, 'get_value', key))
        expected_results.append(0)

        invokes.append(runner.call_contract(path1, 'get_value', key))
        expected_results.append(value)

        runner.execute(get_storage_from=contract_1)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        storage_result = runner.storages.get(contract_1, key)
        self.assertEqual(value, storage_result.as_int())

    def test_create_map(self):
        path, _ = self.get_deploy_file_paths('StorageCreateMap.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        map_key = b'example_'
        storage_key = b'test1'
        stored_value = b'123'

        invokes.append(runner.call_contract(path, 'get_from_map', storage_key,
                                            expected_result_type=bytes))
        expected_results.append(b'')
        storage_contract = invokes[-1].invoke.contract

        invokes.append(runner.call_contract(path, 'insert_to_map', storage_key, stored_value))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'get_from_map', b'test1',
                                            expected_result_type=bytes))
        expected_results.append(stored_value)

        runner.execute(get_storage_from=storage_contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertIsNone(runner.storages.get(storage_contract, storage_key))
        storage_result = runner.storages.get(storage_contract, map_key + storage_key)
        self.assertEqual(stored_value, storage_result.as_bytes())

        invokes.append(runner.call_contract(path, 'delete_from_map', b'test1'))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'get_from_map', b'test1',
                                            expected_result_type=bytes))
        expected_results.append(b'')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_import_storage(self):
        path, _ = self.get_deploy_file_paths('ImportStorage.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        prefix = b'unit'
        key = prefix + b'_test'
        key_str = String.from_bytes(key)
        value = 1234

        invokes.append(runner.call_contract(path, 'get_value', key))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'find_by_prefix', prefix))
        expected_results.append([])

        runner.execute()  # getting result of multiple iterators is failing
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        invokes.append(runner.call_contract(path, 'put_value', key, value))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'get_value', key))
        expected_results.append(value)

        invokes.append(runner.call_contract(path, 'find_by_prefix', prefix))
        expected_results.append([[key_str, Integer(value).to_byte_array()]])

        runner.execute()  # getting result of multiple iterators is failing
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.call_contract(path, 'put_value', key, value)
        runner.call_contract(path, 'get_value', key)

        invokes.append(runner.call_contract(path, 'delete_value', key))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'get_value', key))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'find_by_prefix', prefix))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_import_interop_storage(self):
        path, _ = self.get_deploy_file_paths('ImportInteropStorage.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        prefix = b'unit'
        key = prefix + b'_test'
        key_str = String.from_bytes(key)
        value = 1234

        invokes.append(runner.call_contract(path, 'get_value', key))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'find_by_prefix', prefix))
        expected_results.append([])

        runner.execute()  # getting result of multiple iterators is failing
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        invokes.append(runner.call_contract(path, 'put_value', key, value))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'get_value', key))
        expected_results.append(value)

        invokes.append(runner.call_contract(path, 'find_by_prefix', prefix))
        expected_results.append([[key_str, Integer(value).to_byte_array()]])

        runner.execute()  # getting result of multiple iterators is failing
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        runner.call_contract(path, 'put_value', key, value)
        runner.call_contract(path, 'get_value', key)

        invokes.append(runner.call_contract(path, 'delete_value', key))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'get_value', key))
        expected_results.append(0)

        invokes.append(runner.call_contract(path, 'find_by_prefix', prefix))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_as_read_only(self):
        path, _ = self.get_deploy_file_paths('StorageAsReadOnly.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        key = b'key'
        value_old = 'old value'
        value_new = 'new value'

        # Putting old value in the storage
        invokes.append(runner.call_contract(path, 'put_value_in_storage', key, value_old))
        expected_results.append(None)

        invokes.append(runner.call_contract(path, 'get_value_in_storage_read_only', key))
        expected_results.append(value_old)

        invokes.append(runner.call_contract(path, 'get_value_in_storage', key))
        expected_results.append(value_old)

        invokes.append(runner.call_contract(path, 'get_value_in_storage_read_only', key))
        expected_results.append(value_old)

        invokes.append(runner.call_contract(path, 'get_value_in_storage', key))
        expected_results.append(value_old)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # Trying to put a new value in the storage using read_only won't work
        runner.call_contract(path, 'put_value_in_storage_read_only', key, value_new)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.VALUE_DOES_NOT_FALL_WITHIN_EXPECTED_RANGE_MSG)

    def test_find_options_values(self):
        path, _ = self.get_deploy_file_paths('FindOptionsValues.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', FindOptions.KEYS_ONLY))
        expected_results.append(FindOptions.KEYS_ONLY)

        invokes.append(runner.call_contract(path, 'option_keys_only'))
        expected_results.append(FindOptions.KEYS_ONLY)

        invokes.append(runner.call_contract(path, 'option_remove_prefix'))
        expected_results.append(FindOptions.REMOVE_PREFIX)

        invokes.append(runner.call_contract(path, 'option_values_only'))
        expected_results.append(FindOptions.VALUES_ONLY)

        invokes.append(runner.call_contract(path, 'option_deserialize_values'))
        expected_results.append(FindOptions.DESERIALIZE_VALUES)

        invokes.append(runner.call_contract(path, 'option_pick_field_0'))
        expected_results.append(FindOptions.PICK_FIELD_0)

        invokes.append(runner.call_contract(path, 'option_pick_field_1'))
        expected_results.append(FindOptions.PICK_FIELD_1)

        invokes.append(runner.call_contract(path, 'option_backwards'))
        expected_results.append(FindOptions.BACKWARDS)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_find_options_mismatched_type(self):
        path = self.get_contract_path('FindOptionsMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
