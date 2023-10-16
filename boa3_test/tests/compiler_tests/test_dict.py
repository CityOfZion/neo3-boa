from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestDict(BoaTest):
    default_folder: str = 'test_sc/dict_test'

    def test_dict_int_keys(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.NEWMAP  # a = {1: 15, 2: 14, 3: 13}
            + Opcode.DUP
            + Opcode.PUSH1      # map[1] = 15
            + Opcode.PUSH15
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH2      # map[2] = 14
            + Opcode.PUSH14
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH3      # map[3] = 13
            + Opcode.PUSH13
            + Opcode.SETITEM
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('IntKeyDict.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_dict_str_keys(self):
        one = String('one').to_bytes()
        two = String('two').to_bytes()
        three = String('three').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.NEWMAP  # a = {'one': 1, 'two': 2, 'three': 3}
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['one'] = 1
            + Integer(len(one)).to_byte_array(min_length=1)
            + one
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['two'] = 2
            + Integer(len(two)).to_byte_array(min_length=1)
            + two
            + Opcode.PUSH2
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['three'] = 3
            + Integer(len(three)).to_byte_array(min_length=1)
            + three
            + Opcode.PUSH3
            + Opcode.SETITEM
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('StrKeyDict.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_dict_any_value(self):
        nine = String('nine').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.NEWMAP  # a = {1: True, 2: 4, 3: 'nine'}
            + Opcode.DUP
            + Opcode.PUSH1      # map[1] = True
            + Opcode.PUSHT
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH2      # map[2] = 4
            + Opcode.PUSH4
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH3      # map[3] = 'nine'
            + Opcode.PUSHDATA1
            + Integer(len(nine)).to_byte_array(min_length=1)
            + nine
            + Opcode.SETITEM
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('AnyValueDict.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_dict_of_dicts(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.NEWMAP  # a = map
            + Opcode.DUP
            + Opcode.PUSH1      # map[1] = {14: False, 12: True, 5: True}
            + Opcode.NEWMAP
            + Opcode.DUP
            + Opcode.PUSH14
            + Opcode.PUSHF
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH12
            + Opcode.PUSHT
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH5
            + Opcode.PUSHT
            + Opcode.SETITEM
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH2      # map[2] = {0: True, 6: False}
            + Opcode.NEWMAP
            + Opcode.DUP
            + Opcode.PUSH0
            + Opcode.PUSHT
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH6
            + Opcode.PUSHF
            + Opcode.SETITEM
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH3      # map[3] = {11: False}
            + Opcode.NEWMAP
            + Opcode.DUP
            + Opcode.PUSH11
            + Opcode.PUSHF
            + Opcode.SETITEM
            + Opcode.SETITEM
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('DictOfDict.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_dict_assign_empty_dict(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.NEWMAP  # a = {}
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('EmptyDictAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_dict_type_hint_assignment(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.NEWMAP  # a = {1: 15, 2: 14, 3: 13}
            + Opcode.DUP
            + Opcode.PUSH1      # map[1] = 15
            + Opcode.PUSH15
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH2      # map[2] = 14
            + Opcode.PUSH14
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH3      # map[3] = 13
            + Opcode.PUSH13
            + Opcode.SETITEM
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('TypeHintAssignment.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_dict_variable_keys_and_values(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x04'
            + b'\x00'
            + Opcode.PUSH1   # a = 1
            + Opcode.STLOC0
            + Opcode.PUSH2   # b = 2
            + Opcode.STLOC1
            + Opcode.PUSH3   # c = 3
            + Opcode.STLOC2
            + Opcode.NEWMAP  # d = {a: c, b: a, c: b}
            + Opcode.DUP
            + Opcode.PUSH1      # map[a] = c
            + Opcode.PUSH3
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH2      # map[b] = a
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH3      # map[c] = b
            + Opcode.PUSH2
            + Opcode.SETITEM
            + Opcode.STLOC3
            + Opcode.RET
        )

        path = self.get_contract_path('VariableDict.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_dict_get_value(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET
        )

        path = self.get_contract_path('GetValue.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', {0: 'zero'}))
        expected_results.append('zero')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', {1: 'one'})
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.MAP_KEY_NOT_FOUND_ERROR_MSG)

    def test_dict_get_value_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeGetValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_dict_set_value(self):
        ok = String('ok').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH0
            + Opcode.PUSHDATA1
            + Integer(len(ok)).to_byte_array(min_length=1)
            + ok
            + Opcode.SETITEM
            + Opcode.LDARG0
            + Opcode.RET
        )

        path = self.get_contract_path('SetValue.py')
        output = self.assertCompilerNotLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', {0: 'zero'}))
        expected_results.append({0: 'ok'})
        invokes.append(runner.call_contract(path, 'Main', {1: 'one'}))
        expected_results.append({0: 'ok', 1: 'one'})

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_dict_set_value_mismatched_type(self):
        path = self.get_contract_path('MismatchedTypeSetValue.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_dict_keys(self):
        one = String('one').to_bytes()
        two = String('two').to_bytes()
        three = String('three').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.NEWMAP  # a = {'one': 1, 'two': 2, 'three': 3}
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['one'] = 1
            + Integer(len(one)).to_byte_array(min_length=1)
            + one
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['two'] = 2
            + Integer(len(two)).to_byte_array(min_length=1)
            + two
            + Opcode.PUSH2
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['three'] = 3
            + Integer(len(three)).to_byte_array(min_length=1)
            + three
            + Opcode.PUSH3
            + Opcode.SETITEM
            + Opcode.STLOC0
            + Opcode.LDLOC0  # b = a.keys()
            + Opcode.KEYS
            + Opcode.STLOC1
            + Opcode.LDLOC1  # return b
            + Opcode.RET
        )

        path = self.get_contract_path('KeysDict.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(['one', 'two', 'three'])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_dict_keys_mismatched_type(self):
        one = String('one').to_bytes()
        two = String('two').to_bytes()
        three = String('three').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.NEWMAP  # a = {'one': 1, 'two': 2, 'three': 3}
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['one'] = 1
            + Integer(len(one)).to_byte_array(min_length=1)
            + one
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['two'] = 2
            + Integer(len(two)).to_byte_array(min_length=1)
            + two
            + Opcode.PUSH2
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['three'] = 3
            + Integer(len(three)).to_byte_array(min_length=1)
            + three
            + Opcode.PUSH3
            + Opcode.SETITEM
            + Opcode.STLOC0
            + Opcode.LDLOC0  # b = a.keys()
            + Opcode.KEYS
            + Opcode.STLOC1
            + Opcode.LDLOC1  # return b
            + Opcode.RET
        )

        path = self.get_contract_path('MismatchedTypeKeysDict.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(['one', 'two', 'three'])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_dict_values(self):
        one = String('one').to_bytes()
        two = String('two').to_bytes()
        three = String('three').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.NEWMAP  # a = {'one': 1, 'two': 2, 'three': 3}
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['one'] = 1
            + Integer(len(one)).to_byte_array(min_length=1)
            + one
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['two'] = 2
            + Integer(len(two)).to_byte_array(min_length=1)
            + two
            + Opcode.PUSH2
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['three'] = 3
            + Integer(len(three)).to_byte_array(min_length=1)
            + three
            + Opcode.PUSH3
            + Opcode.SETITEM
            + Opcode.STLOC0
            + Opcode.LDLOC0  # b = a.values()
            + Opcode.VALUES
            + Opcode.STLOC1
            + Opcode.LDLOC1  # return b
            + Opcode.RET
        )

        path = self.get_contract_path('ValuesDict.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 2, 3])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_dict_values_mismatched_type(self):
        one = String('one').to_bytes()
        two = String('two').to_bytes()
        three = String('three').to_bytes()

        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.NEWMAP  # a = {'one': 1, 'two': 2, 'three': 3}
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['one'] = 1
            + Integer(len(one)).to_byte_array(min_length=1)
            + one
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['two'] = 2
            + Integer(len(two)).to_byte_array(min_length=1)
            + two
            + Opcode.PUSH2
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSHDATA1  # map['three'] = 3
            + Integer(len(three)).to_byte_array(min_length=1)
            + three
            + Opcode.PUSH3
            + Opcode.SETITEM
            + Opcode.STLOC0
            + Opcode.LDLOC0  # b = a.values()
            + Opcode.VALUES
            + Opcode.STLOC1
            + Opcode.LDLOC1  # return b
            + Opcode.RET
        )

        path = self.get_contract_path('MismatchedTypeValuesDict.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 2, 3])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_dict_boa2_test2(self):
        path, _ = self.get_deploy_file_paths('DictBoa2Test2.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(7)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_dict_any_key_and_value(self):
        path, _ = self.get_deploy_file_paths('DictAnyKeyAndValue.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(66)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_dict_test1(self):
        path, _ = self.get_deploy_file_paths('DictBoa2Test1.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invoke = runner.call_contract(path, 'main')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        from typing import Dict
        self.assertIsInstance(invoke.result, Dict)

    def test_boa2_dict_test3(self):
        path, _ = self.get_deploy_file_paths('DictBoa2Test3.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        from typing import Dict
        self.assertIsInstance(invoke.result, Dict)
        self.assertEqual({}, invoke.result)

    def test_boa2_dict_test4(self):
        path, _ = self.get_deploy_file_paths('DictBoa2Test4.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_dict_test5_should_not_compile(self):
        # this doesn't compile in boa2, but should compile here
        path, _ = self.get_deploy_file_paths('DictBoa2Test5ShouldNotCompile.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append({'a': 2})

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_dict_test6_should_not_compile(self):
        # this doesn't compile in boa2, but should compile here
        path, _ = self.get_deploy_file_paths('DictBoa2Test6ShouldNotCompile.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append({'a': 1, 'b': 2})

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_dict_test_keys(self):
        path, _ = self.get_deploy_file_paths('DictBoa2TestKeys.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append('abblahmzmcallltrs')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_dict_test_values(self):
        path, _ = self.get_deploy_file_paths('DictBoa2TestValues.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(55)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_dict_pop(self):
        path, _ = self.get_deploy_file_paths('DictPop.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'a'
        invokes.append(runner.call_contract(path, 'main', dict_, key))
        value = dict_.pop(key)
        expected_results.append([dict_, value])

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'd'
        invokes.append(runner.call_contract(path, 'main', dict_, key))
        value = dict_.pop(key)
        expected_results.append([dict_, value])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'key not inside'
        runner.call_contract(path, 'main', dict_, key)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.MAP_KEY_NOT_FOUND_ERROR_MSG)
        self.assertRaises(KeyError, dict_.pop, key)

    def test_dict_pop_default(self):
        path, _ = self.get_deploy_file_paths('DictPopDefault.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'a'
        default = 'test'
        invokes.append(runner.call_contract(path, 'main', dict_, key, default))
        value = dict_.pop(key, default)
        expected_results.append([dict_, value])

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'd'
        default = 'test'
        invokes.append(runner.call_contract(path, 'main', dict_, key, default))
        value = dict_.pop(key, default)
        expected_results.append([dict_, value])

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'not inside'
        default = 'test'
        invokes.append(runner.call_contract(path, 'main', dict_, key, default))
        value = dict_.pop(key, default)
        expected_results.append([dict_, value])

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'not inside'
        default = 123456
        invokes.append(runner.call_contract(path, 'main', dict_, key, default))
        value = dict_.pop(key, default)
        expected_results.append([dict_, value])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_dict_copy(self):
        path, _ = self.get_deploy_file_paths('DictCopy.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        _dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
        invokes.append(runner.call_contract(path, 'copy_dict', _dict))
        expected_results.append([{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5},
                                 {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'unit': 'test'}
                                 ])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_dict_copy_builtin_call(self):
        path, _ = self.get_deploy_file_paths('CopyDictBuiltinCall.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'copy_dict', {0: 10, 1: 11, 2: 12}, 3, 13))
        expected_results.append([{0: 10, 1: 11, 2: 12},
                                 {0: 10, 1: 11, 2: 12, 3: 13}
                                 ])

        invokes.append(runner.call_contract(path, 'copy_dict', {'dict': 1, 'unit': 2, 'test': 3}, 'copy', 4))
        expected_results.append([{'dict': 1, 'unit': 2, 'test': 3},
                                 {'dict': 1, 'unit': 2, 'test': 3, 'copy': 4}
                                 ])

        invokes.append(runner.call_contract(path, 'copy_dict', {True: 1, False: 0}, True, 99))
        expected_results.append([{True: 1, False: 0},
                                 {True: 99, False: 0}
                                 ])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_del_dict_pair(self):
        path = self.get_contract_path('DelPair.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)
