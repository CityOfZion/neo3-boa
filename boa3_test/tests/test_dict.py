from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest


class TestDict(BoaTest):

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
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/dict_test/IntKeyDict.py' % self.dirname
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
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/dict_test/StrKeyDict.py' % self.dirname
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
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/dict_test/AnyValueDict.py' % self.dirname
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
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/dict_test/DictOfDict.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_dict_assign_empty_dict(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.NEWMAP  # a = {}
            + Opcode.STLOC0
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/dict_test/EmptyDictAssignment.py' % self.dirname
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
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/dict_test/TypeHintAssignment.py' % self.dirname
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
            + Opcode.LDLOC0     # map[a] = c
            + Opcode.LDLOC2
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.LDLOC1     # map[b] = a
            + Opcode.LDLOC0
            + Opcode.SETITEM
            + Opcode.DUP
            + Opcode.LDLOC2     # map[c] = b
            + Opcode.LDLOC1
            + Opcode.SETITEM
            + Opcode.STLOC3
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/dict_test/VariableDict.py' % self.dirname
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

        path = '%s/boa3_test/test_sc/dict_test/GetValue.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_dict_get_value_mismatched_type(self):
        path = '%s/boa3_test/test_sc/dict_test/MismatchedTypeGetValue.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

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

        path = '%s/boa3_test/test_sc/dict_test/SetValue.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_dict_set_value_mismatched_type(self):
        path = '%s/boa3_test/test_sc/dict_test/MismatchedTypeSetValue.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

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

        path = '%s/boa3_test/test_sc/dict_test/KeysDict.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_dict_keys_mismatched_type(self):
        path = '%s/boa3_test/test_sc/dict_test/MismatchedTypeKeysDict.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

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

        path = '%s/boa3_test/test_sc/dict_test/ValuesDict.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_dict_values_mismatched_type(self):
        path = '%s/boa3_test/test_sc/dict_test/MismatchedTypeValuesDict.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)
