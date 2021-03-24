from boa3.boa3 import Boa3
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestNone(BoaTest):

    default_folder: str = 'test_sc/none_test'

    def test_variable_none(self):
        path = self.get_contract_path('VariableNone.py')

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHNULL
            + Opcode.STLOC0
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_none_tuple(self):
        path = self.get_contract_path('NoneTuple.py')

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHNULL   # a = (None, None, None)
            + Opcode.PUSHNULL
            + Opcode.PUSHNULL
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.RET        # return
        )
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_none_identity(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.ISNULL
            + Opcode.RET        # return
        )

        path = self.get_contract_path('NoneIdentity.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', None)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', 5)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', '5')
        self.assertEqual(False, result)

    def test_none_not_identity(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.ISNULL
            + Opcode.NOT
            + Opcode.RET        # return
        )

        path = self.get_contract_path('NoneNotIdentity.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', None)
        self.assertEqual(False, result)
        result = self.run_smart_contract(engine, path, 'Main', 5)
        self.assertEqual(True, result)
        result = self.run_smart_contract(engine, path, 'Main', '5')
        self.assertEqual(True, result)

    def test_none_equality(self):
        path = self.get_contract_path('NoneEquality.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_mismatched_type_int_operation(self):
        path = self.get_contract_path('MismatchedTypesInOperation.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_reassign_variable_with_none(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH2          # a = 2
            + Opcode.STLOC0
            + Opcode.PUSH4          # b = a * 2
            + Opcode.STLOC1
            + Opcode.PUSHNULL       # a = None
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('ReassignVariableWithNone.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_reassign_variable_after_none(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHNULL       # a = None
            + Opcode.STLOC0
            + Opcode.PUSH2          # a = 2
            + Opcode.STLOC0
            + Opcode.PUSH4          # b = a * 2
            + Opcode.STLOC1
            + Opcode.RET        # return
        )
        path = self.get_contract_path('ReassignVariableAfterNone.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

    def test_boa2_none_test(self):
        path = self.get_contract_path('NoneBoa2Test.py')
        self.assertCompilerLogs(MismatchedTypes, path)
