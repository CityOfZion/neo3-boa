from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestTyping(boatestcase.BoaTestCase):
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

        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, 'CastToInt.py')
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

        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, 'CastToStr.py')
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

        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, 'CastToList.py')
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
            + Opcode.PICKITEM
            + Opcode.RET
        )

        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, 'CastToTypedList.py')
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

        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, 'CastToDict.py')
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

        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, 'CastToTypedDict.py')
        self.assertEqual(expected_output, output)

    def test_cast_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'CastMismatchedType.py')

    def test_cast_to_uint160_compile(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0     # x = cast(UInt160, value)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return x
            + Opcode.RET
        )

        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, 'CastToUInt160.py')
        self.assertEqual(expected_output, output)

    async def test_cast_to_uint160_run(self):
        await self.set_up_contract('CastToUInt160.py')

        value = bytes(range(20))
        result, _ = await self.call('Main', [value], return_type=bytes)
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

        output, _ = self.assertCompilerLogs(CompilerWarning.TypeCasting, 'CastToTransaction.py')
        self.assertEqual(expected_output, output)

    async def test_cast_inside_if(self):
        await self.set_up_contract('CastInsideIf.py')

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual('body', result)

    async def test_cast_persisted_in_scope(self):
        await self.set_up_contract('CastPersistedInScope.py')

        test_address = bytes(20)
        result, _ = await self.call('main', [test_address, 10, None], return_type=None)
        self.assertIsNone(result)
