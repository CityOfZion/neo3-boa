from boa3.neo.vm.type.String import String

from boa3.boa3 import Boa3
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.StackItemType import StackItemType
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestAssert(BoaTest):

    assert_resulted_false_msg = 'ASSERT is executed with false result.'

    def test_assert_unary_boolean_operation(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0     # assert not a
            + Opcode.NOT
            + Opcode.ASSERT
            + Opcode.LDARG1     # return b
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/assert_test/AssertUnaryOperation.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', False, 10)
        self.assertEqual(10, result)

        with self.assertRaises(TestExecutionException, msg=self.assert_resulted_false_msg):
            self.run_smart_contract(engine, path, 'Main', True, 20)

    def test_assert_binary_boolean_operation(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0     # assert a != b
            + Opcode.LDARG1
            + Opcode.NUMNOTEQUAL
            + Opcode.ASSERT
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/assert_test/AssertBinaryOperation.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 10, 20)
        self.assertEqual(10, result)

        with self.assertRaises(TestExecutionException, msg=self.assert_resulted_false_msg):
            self.run_smart_contract(engine, path, 'Main', 20, 20)

    def test_assert_with_message(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a > 0, 'a must be greater than zero'
            + Opcode.PUSH0
            + Opcode.GT
            + Opcode.ASSERT         # neo assert doesn't receive messages yet
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/assert_test/AssertWithMessage.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(10, result)

        with self.assertRaises(TestExecutionException, msg=self.assert_resulted_false_msg):
            self.run_smart_contract(engine, path, 'Main', -10)

    def test_assert_int(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.ASSERT
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/assert_test/AssertInt.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 10)
        self.assertEqual(10, result)
        result = self.run_smart_contract(engine, path, 'Main', -10)
        self.assertEqual(-10, result)

        with self.assertRaises(TestExecutionException, msg=self.assert_resulted_false_msg):
            self.run_smart_contract(engine, path, 'Main', 0)

    def test_assert_str(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.ASSERT
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/assert_test/AssertStr.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', 'unittest')
        self.assertEqual('unittest', result)

        with self.assertRaises(TestExecutionException, msg=self.assert_resulted_false_msg):
            self.run_smart_contract(engine, path, 'Main', '')

    def test_assert_bytes(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.ASSERT
            + Opcode.LDARG0     # return a
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/assert_test/AssertBytes.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', b'unittest')
        self.assertEqual(b'unittest', String(result).to_bytes())

        with self.assertRaises(TestExecutionException, msg=self.assert_resulted_false_msg):
            self.run_smart_contract(engine, path, 'Main', b'')

    def test_assert_list(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.SIZE
            + Opcode.ASSERT
            + Opcode.LDARG0     # return len(a)
            + Opcode.SIZE
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/assert_test/AssertList.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', [1, 2, 3])
        self.assertEqual(3, result)

        with self.assertRaises(TestExecutionException, msg=self.assert_resulted_false_msg):
            self.run_smart_contract(engine, path, 'Main', [])

    def test_assert_dict(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.SIZE
            + Opcode.ASSERT
            + Opcode.LDARG0     # return len(a)
            + Opcode.SIZE
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/assert_test/AssertDict.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main', {1: 2, 2: 5})
        self.assertEqual(2, result)

        with self.assertRaises(TestExecutionException, msg=self.assert_resulted_false_msg):
            self.run_smart_contract(engine, path, 'Main', {})

    def test_assert_any(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # assert a
            + Opcode.DUP
            + Opcode.ISTYPE + StackItemType.Array
            + Opcode.JMPIF + Integer(12).to_byte_array(signed=True, min_length=1)
            + Opcode.DUP
            + Opcode.ISTYPE + StackItemType.Map
            + Opcode.JMPIF + Integer(7).to_byte_array(signed=True, min_length=1)
            + Opcode.DUP
            + Opcode.ISTYPE + StackItemType.Struct
            + Opcode.JMPIFNOT + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.SIZE
            + Opcode.ASSERT
            + Opcode.PUSHNULL
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/assert_test/AssertAny.py' % self.dirname
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)
