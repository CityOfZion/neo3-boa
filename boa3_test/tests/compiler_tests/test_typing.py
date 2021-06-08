from boa3.exception import CompilerError, CompilerWarning
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestTyping(BoaTest):

    default_folder: str = 'test_sc/typing_test'

    def test_cast_to_int(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # x = cast(int, value)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        path = self.get_contract_path('CastToInt.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_cast_to_str(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # x = cast(str, value)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        path = self.get_contract_path('CastToStr.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_cast_to_list(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # x = cast(list, value)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        path = self.get_contract_path('CastToList.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_cast_to_typed_list(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # x = cast(List[int], value)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return x[0]
            + Opcode.PUSH0
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET
        )

        path = self.get_contract_path('CastToTypedList.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_cast_to_dict(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # x = cast(dict, value)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        path = self.get_contract_path('CastToDict.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_cast_to_typed_dict(self):
        string = String('example').to_bytes()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # x = cast(Dict[str, int], value)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return x['example']
            + Opcode.PUSHDATA1
            + Integer(len(string)).to_byte_array(min_length=1)
            + string
            + Opcode.PICKITEM
            + Opcode.RET
        )

        path = self.get_contract_path('CastToTypedDict.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_cast_mismatched_type(self):
        path = self.get_contract_path('CastMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_cast_to_uint160(self):
        path = self.get_contract_path('CastToUInt160.py')
        self.assertCompilerLogs(CompilerWarning.TypeCasting, path)

        engine = TestEngine()
        value = bytes(range(20))
        result = self.run_smart_contract(engine, path, 'Main', value,
                                         expected_result_type=bytes)
        self.assertEqual(value, result)

    def test_cast_to_transaction(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # x = cast(Transaction, value)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        path = self.get_contract_path('CastToTransaction.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)
