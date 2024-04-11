from typing import Any

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestDict(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/dict_test'
    MAP_KEY_NOT_FOUND_ERROR_MSG = 'Key not found in Map'

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

        output, _ = self.assertCompile('IntKeyDict.py')
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

        output, _ = self.assertCompile('StrKeyDict.py')
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

        output, _ = self.assertCompile('AnyValueDict.py')
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

        output, _ = self.assertCompile('DictOfDict.py')
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

        output, _ = self.assertCompile('EmptyDictAssignment.py')
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

        output, _ = self.assertCompile('TypeHintAssignment.py')
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

        output, _ = self.assertCompile('VariableDict.py')
        self.assertEqual(expected_output, output)

    def test_dict_get_value_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET
        )

        output, _ = self.assertCompile('DictGetValue.py')
        self.assertEqual(expected_output, output)

    async def test_dict_get_value(self):
        await self.set_up_contract('DictGetValue.py')

        result, _ = await self.call('Main', [{0: 'zero'}], return_type=str)
        self.assertEqual('zero', result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('Main', [{1: 'one'}], return_type=str)

        self.assertRegex(str(context.exception), self.MAP_KEY_NOT_FOUND_ERROR_MSG)

    def test_dict_get_value_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MismatchedTypeDictGetValue.py')

    def test_dict_set_value_compile(self):
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

        path = self.get_contract_path('DictSetValue.py')
        output = self.assertCompilerNotLogs(CompilerWarning.NameShadowing, path)
        self.assertEqual(expected_output, output)

    async def test_dict_set_value(self):
        await self.set_up_contract('DictSetValue.py')

        result, _ = await self.call('Main', [{0: 'zero'}], return_type=dict[int, str])
        self.assertEqual({0: 'ok'}, result)
        result, _ = await self.call('Main', [{1: 'one'}], return_type=dict[int, str])
        self.assertEqual({0: 'ok', 1: 'one'}, result)

    def test_dict_set_value_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MismatchedTypeDictSetValue.py')

    def test_dict_keys_compile(self):
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

        output, _ = self.assertCompile('KeysDict.py')
        self.assertEqual(expected_output, output)

    async def test_dict_keys(self):
        await self.set_up_contract('KeysDict.py')

        result, _ = await self.call('Main', [], return_type=list[str])
        self.assertEqual(['one', 'two', 'three'], result)

    def test_dict_keys_mismatched_type_compile(self):
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

        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, 'MismatchedTypeKeysDict.py')
        self.assertEqual(expected_output, output)

    async def test_dict_keys_mismatched_type(self):
        await self.set_up_contract('MismatchedTypeKeysDict.py')

        result, _ = await self.call('Main', [], return_type=list[str])
        self.assertEqual(['one', 'two', 'three'], result)

    def test_dict_values_compile(self):
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

        output, _ = self.assertCompile('ValuesDict.py')
        self.assertEqual(expected_output, output)

    async def test_dict_values(self):
        await self.set_up_contract('ValuesDict.py')

        result, _ = await self.call('Main', [], return_type=list[int])
        self.assertEqual([1, 2, 3], result)

    def test_dict_values_mismatched_type_compile(self):
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

        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, 'MismatchedTypeValuesDict.py')
        self.assertEqual(expected_output, output)

    async def test_dict_values_mismatched_type(self):
        await self.set_up_contract('MismatchedTypeValuesDict.py')

        result, _ = await self.call('Main', [], return_type=list)
        self.assertEqual([1, 2, 3], result)

    async def test_dict_boa2_test2(self):
        await self.set_up_contract('DictBoa2Test2.py')

        result, _ = await self.call('Main', [], return_type=int)
        self.assertEqual(7, result)

    async def test_dict_any_key_and_value(self):
        await self.set_up_contract('DictAnyKeyAndValue.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(66, result)

    async def test_boa2_dict_test1(self):
        await self.set_up_contract('DictBoa2Test1.py')

        result, _ = await self.call('main', [], return_type=dict)

        self.assertIsInstance(result, dict)

    async def test_boa2_dict_test3(self):
        await self.set_up_contract('DictBoa2Test3.py')

        result, _ = await self.call('main', [], return_type=dict)

        self.assertIsInstance(result, dict)
        self.assertEqual({}, result)

    async def test_boa2_dict_test4(self):
        await self.set_up_contract('DictBoa2Test4.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(10, result)

    async def test_boa2_dict_test5_should_not_compile(self):
        # this doesn't compile in boa2, but should compile here
        await self.set_up_contract('DictBoa2Test5ShouldNotCompile.py')

        result, _ = await self.call('main', [], return_type=dict[str, int])
        self.assertEqual({'a': 2}, result)

    async def test_boa2_dict_test6_should_not_compile(self):
        # this doesn't compile in boa2, but should compile here
        await self.set_up_contract('DictBoa2Test6ShouldNotCompile.py')

        result, _ = await self.call('main', [], return_type=dict[str, int])
        self.assertEqual({'a': 1, 'b': 2}, result)

    async def test_boa2_dict_test_keys(self):
        await self.set_up_contract('DictBoa2TestKeys.py')

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual('abblahmzmcallltrs', result)

    async def test_boa2_dict_test_values(self):
        await self.set_up_contract('DictBoa2TestValues.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(55, result)

    async def test_dict_pop(self):
        await self.set_up_contract('DictPop.py')

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'a'
        result, _ = await self.call('main', [dict_, key], return_type=tuple[dict[str, int], int])
        value = dict_.pop(key)
        self.assertEqual((dict_, value), result)

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'd'
        result, _ = await self.call('main', [dict_, key], return_type=tuple[dict[str, int], int])
        value = dict_.pop(key)
        self.assertEqual((dict_, value), result)

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'key not inside'
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [dict_, key], return_type=tuple[dict[str, int], int])

        self.assertRegex(str(context.exception), self.MAP_KEY_NOT_FOUND_ERROR_MSG)
        self.assertRaises(KeyError, dict_.pop, key)

    async def test_dict_pop_default(self):
        await self.set_up_contract('DictPopDefault.py')

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'a'
        default = 'test'
        result, _ = await self.call('main', [dict_, key, default], return_type=tuple[dict[str, int], int])
        value = dict_.pop(key, default)
        self.assertEqual((dict_, value), result)

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'd'
        default = 'test'
        result, _ = await self.call('main', [dict_, key, default], return_type=tuple[dict[str, int], int])
        value = dict_.pop(key, default)
        self.assertEqual((dict_, value), result)

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'not inside'
        default = 'test'
        result, _ = await self.call('main', [dict_, key, default], return_type=tuple[dict[str, int], int])
        value = dict_.pop(key, default)
        self.assertEqual((dict_, value), result)

        dict_ = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        key = 'not inside'
        default = 123456
        result, _ = await self.call('main', [dict_, key, default], return_type=tuple[dict[str, int], int])
        value = dict_.pop(key, default)
        self.assertEqual((dict_, value), result)

    async def test_dict_copy(self):
        await self.set_up_contract('DictCopy.py')

        _dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
        result, _ = await self.call('copy_dict', [_dict], return_type=list[dict[str, Any]])
        self.assertEqual([{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}, {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'unit': 'test'}], result)

    async def test_dict_copy_builtin_call(self):
        await self.set_up_contract('CopyDictBuiltinCall.py')

        result, _ = await self.call('copy_dict', [{0: 10, 1: 11, 2: 12}, 3, 13], return_type=tuple[dict, dict])
        self.assertEqual(({0: 10, 1: 11, 2: 12}, {0: 10, 1: 11, 2: 12, 3: 13}), result)

        result, _ = await self.call('copy_dict', [{'dict': 1, 'unit': 2, 'test': 3}, 'copy', 4], return_type=tuple[dict[str, Any], dict[str, Any]])
        self.assertEqual(({'dict': 1, 'unit': 2, 'test': 3}, {'dict': 1, 'unit': 2, 'test': 3, 'copy': 4}), result)

        result, _ = await self.call('copy_dict', [{True: 1, False: 0}, True, 99], return_type=tuple[dict, dict])
        self.assertEqual(({True: 1, False: 0}, {True: 99, False: 0}), result)

    def test_del_dict_pair(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'DelPair.py')
