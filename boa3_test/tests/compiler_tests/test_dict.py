from boa3.boa3 import Boa3
from boa3.exception import CompilerError, CompilerWarning
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


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
        output = Boa3.compile(path)
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
        output = Boa3.compile(path)
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
            + Opcode.PUSH1
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
        output = Boa3.compile(path)
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
            + Opcode.PUSH0
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH12
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH5
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH2      # map[2] = {0: True, 6: False}
            + Opcode.NEWMAP
            + Opcode.DUP
            + Opcode.PUSH0
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH6
            + Opcode.PUSH0
            + Opcode.SETITEM
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.PUSH3      # map[3] = {11: False}
            + Opcode.NEWMAP
            + Opcode.DUP
            + Opcode.PUSH11
            + Opcode.PUSH0
            + Opcode.SETITEM
            + Opcode.SETITEM
            + Opcode.STLOC0
            + Opcode.RET
        )

        path = self.get_contract_path('DictOfDict.py')
        output = Boa3.compile(path)
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
        output = Boa3.compile(path)
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
        output = Boa3.compile(path)
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
        output = Boa3.compile(path)
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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', {0: 'zero'})
        self.assertEqual('zero', result)

        with self.assertRaises(TestExecutionException, msg=self.MAP_KEY_NOT_FOUND_ERROR_MSG):
            self.run_smart_contract(engine, path, 'Main', {1: 'one'})

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', {0: 'zero'})
        self.assertEqual({0: 'ok'}, result)
        result = self.run_smart_contract(engine, path, 'Main', {1: 'one'})
        self.assertEqual({0: 'ok', 1: 'one'}, result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(['one', 'two', 'three'], result)

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

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(['one', 'two', 'three'], result)

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
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3], result)

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

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual([1, 2, 3], result)

    def test_dict_boa2_test2(self):
        path = self.get_contract_path('DictBoa2Test2.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual(7, result)

    def test_dict_any_key_and_value(self):
        path = self.get_contract_path('DictAnyKeyAndValue.py')
        Boa3.compile_and_save(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(66, result)

    def test_boa2_dict_test1(self):
        path = self.get_contract_path('DictBoa2Test1.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        from typing import Dict
        self.assertIsInstance(result, Dict)

    def test_boa2_dict_test3(self):
        path = self.get_contract_path('DictBoa2Test3.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        from typing import Dict
        self.assertIsInstance(result, Dict)
        self.assertEqual(result, {})

    def test_boa2_dict_test4(self):
        path = self.get_contract_path('DictBoa2Test4.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(10, result)

    def test_boa2_dict_test5_should_not_compile(self):
        # this doesn't compile in boa2, but should compile here
        path = self.get_contract_path('DictBoa2Test5ShouldNotCompile.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(result, {'a': 2})

    def test_boa2_dict_test6_should_not_compile(self):
        # this doesn't compile in boa2, but should compile here
        path = self.get_contract_path('DictBoa2Test6ShouldNotCompile.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(result, {'a': 1, 'b': 2})

    def test_boa2_dict_test_keys(self):
        path = self.get_contract_path('DictBoa2TestKeys.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual('abblahmzmcallltrs', result)

    def test_boa2_dict_test_values(self):
        path = self.get_contract_path('DictBoa2TestValues.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(55, result)
