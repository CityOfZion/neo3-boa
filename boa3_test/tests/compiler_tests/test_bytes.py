from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.StackItem import StackItemType
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestBytes(BoaTest):
    default_folder: str = 'test_sc/bytes_test'

    SUBSEQUENCE_NOT_FOUND_MSG = 'subsequence of bytes not found'

    def test_bytes_literal_value(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = b'\x01\x02\x03'
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytesLiteral.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_bytes_get_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytesGetValue.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', bytes([1, 2, 3])))
        expected_results.append(1)
        invokes.append(runner.call_contract(path, 'Main', b'0'))
        expected_results.append(48)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_get_value_negative_index(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSHM1
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytesGetValueNegativeIndex.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', bytes([1, 2, 3])))
        expected_results.append(3)
        invokes.append(runner.call_contract(path, 'Main', b'0'))
        expected_results.append(48)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_set_value(self):
        path = self.get_contract_path('BytesSetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_bytes_clear(self):
        path = self.get_contract_path('BytesClear.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bytes_reverse(self):
        path = self.get_contract_path('BytesReverse.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bytes_to_int(self):
        path, _ = self.get_deploy_file_paths('BytesToInt.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'bytes_to_int'))
        expected_results.append(513)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_to_int_with_builtin(self):
        path = self.get_contract_path('BytesToIntWithBuiltin.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_bytes_to_bool(self):
        path, _ = self.get_deploy_file_paths('BytesToBool.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'bytes_to_bool', b'\x00'))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'bytes_to_bool', b'\x01'))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'bytes_to_bool', b'\x02'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_to_bool_with_builtin(self):
        path = self.get_contract_path('BytesToBoolWithBuiltin.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_bytes_to_str(self):
        path, _ = self.get_deploy_file_paths('BytesToStr.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'bytes_to_str'))
        expected_results.append('abc')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_to_str_with_builtin(self):
        path = self.get_contract_path('BytesToStrWithBuiltin.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_bytes_from_byte_array(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = bytearray(b'\x01\x02\x03')
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.CONVERT + StackItemType.Buffer
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = a
            + Opcode.STLOC1
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytesFromBytearray.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_assign_with_slice(self):
        path, _ = self.get_deploy_file_paths('AssignSlice.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', b'unittest',
                                            expected_result_type=bytearray))
        expected_results.append(b'unittest'[1:2])

        invokes.append(runner.call_contract(path, 'main', b'123',
                                            expected_result_type=bytearray))
        expected_results.append(b'123'[1:2])

        invokes.append(runner.call_contract(path, 'main', bytearray(),
                                            expected_result_type=bytearray))
        expected_results.append(bytearray()[1:2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_slice_with_cast(self):
        path, _ = self.get_deploy_file_paths('SliceWithCast.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', b'unittest',
                                            expected_result_type=bytes))
        expected_results.append(b'unittest'[1:2])

        invokes.append(runner.call_contract(path, 'main', '123',
                                            expected_result_type=bytes))
        expected_results.append(b'123'[1:2])

        invokes.append(runner.call_contract(path, 'main', 12345,
                                            expected_result_type=bytes))
        expected_results.append(Integer(12345).to_byte_array()[1:2])

        invokes.append(runner.call_contract(path, 'main', bytearray(),
                                            expected_result_type=bytearray))
        expected_results.append(bytearray()[1:2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_slice_with_stride(self):
        path, _ = self.get_deploy_file_paths('SliceWithStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = b'unit_test'
        expected_result = a[2:5:2]
        invokes.append(runner.call_contract(path, 'literal_values',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[-6:5:2]
        invokes.append(runner.call_contract(path, 'negative_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[0:-1:2]
        invokes.append(runner.call_contract(path, 'negative_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[-6:-1:2]
        invokes.append(runner.call_contract(path, 'negative_values',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[-999:5:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[0:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[-999:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_values',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[999:5:2]
        invokes.append(runner.call_contract(path, 'really_high_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[0:999:2]
        invokes.append(runner.call_contract(path, 'really_high_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[999:999:2]
        invokes.append(runner.call_contract(path, 'really_high_values',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_slice_with_negative_stride(self):
        path, _ = self.get_deploy_file_paths('SliceWithNegativeStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = b'unit_test'
        expected_result = a[2:5:-1]
        invokes.append(runner.call_contract(path, 'literal_values',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[-6:5:-1]
        invokes.append(runner.call_contract(path, 'negative_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[0:-1:-1]
        invokes.append(runner.call_contract(path, 'negative_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[-6:-1:-1]
        invokes.append(runner.call_contract(path, 'negative_values',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[-999:5:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[0:-999:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[-999:-999:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_values',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[999:5:-1]
        invokes.append(runner.call_contract(path, 'really_high_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[0:999:-1]
        invokes.append(runner.call_contract(path, 'really_high_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[999:999:-1]
        invokes.append(runner.call_contract(path, 'really_high_values',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_slice_omitted_with_stride(self):
        path, _ = self.get_deploy_file_paths('SliceOmittedWithStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = b'unit_test'
        expected_result = a[::2]
        invokes.append(runner.call_contract(path, 'omitted_values',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[:5:2]
        invokes.append(runner.call_contract(path, 'omitted_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[2::2]
        invokes.append(runner.call_contract(path, 'omitted_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[-6::2]
        invokes.append(runner.call_contract(path, 'negative_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[:-1:2]
        invokes.append(runner.call_contract(path, 'negative_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[-999::2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[999::2]
        invokes.append(runner.call_contract(path, 'really_high_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[:999:2]
        invokes.append(runner.call_contract(path, 'really_high_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_slice_omitted_with_negative_stride(self):
        path, _ = self.get_deploy_file_paths('SliceOmittedWithNegativeStride.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        a = b'unit_test'
        expected_result = a[::-2]
        invokes.append(runner.call_contract(path, 'omitted_values',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[:5:-2]
        invokes.append(runner.call_contract(path, 'omitted_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[2::-2]
        invokes.append(runner.call_contract(path, 'omitted_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[-6::-2]
        invokes.append(runner.call_contract(path, 'negative_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[:-1:-2]
        invokes.append(runner.call_contract(path, 'negative_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[-999::-2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[:-999:-2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[999::-2]
        invokes.append(runner.call_contract(path, 'really_high_start',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        a = b'unit_test'
        expected_result = a[:999:-2]
        invokes.append(runner.call_contract(path, 'really_high_end',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_get_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayGetValue.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', bytes([1, 2, 3])))
        expected_results.append(1)
        invokes.append(runner.call_contract(path, 'Main', b'0'))
        expected_results.append(48)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_get_value_negative_index(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # arg[0]
            + Opcode.PUSHM1
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PICKITEM
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayGetValueNegativeIndex.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', bytes([1, 2, 3])))
        expected_results.append(3)
        invokes.append(runner.call_contract(path, 'Main', b'0'))
        expected_results.append(48)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_set_value(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.CONVERT + StackItemType.Buffer
            + Opcode.STLOC0
            + Opcode.LDLOC0     # var[0] = 0x01
            + Opcode.PUSH0
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.LDLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearraySetValue.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', b'123',
                                            expected_result_type=bytes))
        expected_results.append(b'\x0123')
        invokes.append(runner.call_contract(path, 'Main', b'0',
                                            expected_result_type=bytes))
        expected_results.append(b'\x01')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_set_value_negative_index(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.CONVERT + StackItemType.Buffer
            + Opcode.STLOC0
            + Opcode.LDLOC0     # var[-1] = 0x01
            + Opcode.PUSHM1
            + Opcode.DUP
            + Opcode.SIGN
            + Opcode.PUSHM1
            + Opcode.JMPNE
            + Integer(5).to_byte_array(min_length=1, signed=True)
            + Opcode.OVER
            + Opcode.SIZE
            + Opcode.ADD
            + Opcode.PUSH1
            + Opcode.SETITEM
            + Opcode.LDLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearraySetValueNegativeIndex.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', b'123',
                                            expected_result_type=bytes))
        expected_results.append(b'12\x01')
        invokes.append(runner.call_contract(path, 'Main', b'0',
                                            expected_result_type=bytes))
        expected_results.append(b'\x01')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_literal_value(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = bytearray(b'\x01\x02\x03')
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayLiteral.py')
        output = self.assertCompilerLogs(CompilerWarning.TypeCasting, path)
        self.assertEqual(expected_output, output)

    def test_byte_array_default(self):
        expected_output = (
            Opcode.PUSH0      # bytearray()
            + Opcode.NEWBUFFER
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayDefault.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'create_bytearray',
                                            expected_result_type=bytearray))
        expected_results.append(bytearray())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_from_literal_bytes(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = bytearray(b'\x01\x02\x03')
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.CONVERT + StackItemType.Buffer
            + Opcode.STLOC0
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayFromLiteralBytes.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_byte_array_from_variable_bytes(self):
        data = b'\x01\x02\x03'
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x02'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = b'\x01\x02\x03'
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.STLOC0
            + Opcode.PUSHDATA1  # b = bytearray(a)
            + Integer(len(data)).to_byte_array(min_length=1)
            + data
            + Opcode.CONVERT + StackItemType.Buffer
            + Opcode.STLOC1
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayFromVariableBytes.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

    def test_byte_array_from_size(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0     # bytearray(size)
            + Opcode.NEWBUFFER
            + Opcode.RET        # return
        )

        path = self.get_contract_path('BytearrayFromSize.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'create_bytearray', 10,
                                            expected_result_type=bytearray))
        expected_results.append(bytearray(10))

        invokes.append(runner.call_contract(path, 'create_bytearray', 0,
                                            expected_result_type=bytearray))
        expected_results.append(bytearray(0))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # cannot build with negative size
        runner.call_contract(path, 'create_bytearray', -10,
                             expected_result_type=bytes)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.MAX_ITEM_SIZE_EXCEED_MSG_PREFIX}')

    def test_byte_array_from_list_of_int(self):
        path = self.get_contract_path('BytearrayFromListOfInt.py')
        compiler_error_message = self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

        from boa3.internal.model.builtin.builtin import Builtin
        from boa3.internal.model.type.type import Type
        arg_type = Type.list.build([Type.int])
        expected_error = CompilerError.NotSupportedOperation(0, 0, f'{Builtin.ByteArray.identifier}({arg_type.identifier})')
        self.assertEqual(expected_error._error_message, compiler_error_message)

    def test_byte_array_string(self):
        path, _ = self.get_deploy_file_paths('BytearrayFromString.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        # Neo3-boa's bytearray only converts with utf-8 encoding
        string = 'string value'
        invokes.append(runner.call_contract(path, 'main', string, expected_result_type=bytearray))
        expected_results.append(bytearray(string, 'utf-8'))

        string = 'áãõ😀'
        invokes.append(runner.call_contract(path, 'main', string, expected_result_type=bytearray))
        expected_results.append(bytearray(string, 'utf-8'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_string_with_encoding(self):
        path = self.get_contract_path('BytearrayFromStringWithEncoding.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_byte_array_append(self):
        path, _ = self.get_deploy_file_paths('BytearrayAppend.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(b'\x01\x02\x03\x04')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_append_with_builtin(self):
        path, _ = self.get_deploy_file_paths('BytearrayAppendWithBuiltin.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(b'\x01\x02\x03\x04')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_append_mutable_sequence_with_builtin(self):
        path, _ = self.get_deploy_file_paths('BytearrayAppendWithMutableSequence.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(b'\x01\x02\x03\x04')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_clear(self):
        path, _ = self.get_deploy_file_paths('BytearrayClear.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(b'')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_reverse(self):
        path, _ = self.get_deploy_file_paths('BytearrayReverse.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(b'\x03\x02\x01')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_extend(self):
        path, _ = self.get_deploy_file_paths('BytearrayExtend.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(b'\x01\x02\x03\x04\x05\x06')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_extend_with_builtin(self):
        path, _ = self.get_deploy_file_paths('BytearrayExtendWithBuiltin.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(b'\x01\x02\x03\x04\x05\x06')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_to_int(self):
        path, _ = self.get_deploy_file_paths('BytearrayToInt.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'bytes_to_int'))
        expected_results.append(513)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_byte_array_to_int_with_builtin(self):
        path = self.get_contract_path('BytearrayToIntWithBuiltin.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_byte_array_to_int_with_bytes_builtin(self):
        path = self.get_contract_path('BytearrayToIntWithBytesBuiltin.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_boa2_byte_array_test(self):
        path, _ = self.get_deploy_file_paths('BytearrayBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main',
                                            expected_result_type=bytes))
        expected_results.append(b'\t\x01\x02')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_byte_array_test2(self):
        path = self.get_contract_path('BytearrayBoa2Test2.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_boa2_byte_array_test3(self):
        path, _ = self.get_deploy_file_paths('BytearrayBoa2Test3.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(b'\x01\x02\xaa\xfe')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_slice_test(self):
        path, _ = self.get_deploy_file_paths('SliceBoa2Test.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main',
                                            expected_result_type=bytes))
        expected_results.append(b'\x01\x02\x03\x04')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_slice_test2(self):
        path, _ = self.get_deploy_file_paths('SliceBoa2Test2.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main',
                                            expected_result_type=bytes))
        expected_results.append(b'\x02\x03\x04\x02\x03\x04\x05\x06\x01\x02\x03\x04\x03\x04')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_uint160_bytes(self):
        path, _ = self.get_deploy_file_paths('UInt160Bytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main',
                                            expected_result_type=bytes))
        expected_results.append(b'0123456789abcdefghij')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_uint160_int(self):
        path, _ = self.get_deploy_file_paths('UInt160Int.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main',
                                            expected_result_type=bytes))
        expected_results.append((160).to_bytes(2, 'little') + bytes(18))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_uint256_bytes(self):
        path, _ = self.get_deploy_file_paths('UInt256Bytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main',
                                            expected_result_type=bytes))
        expected_results.append(b'0123456789abcdefghijklmnopqrstuv')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_uint256_int(self):
        path, _ = self.get_deploy_file_paths('UInt256Int.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main',
                                            expected_result_type=bytes))
        expected_results.append((256).to_bytes(2, 'little') + bytes(30))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_upper(self):
        path, _ = self.get_deploy_file_paths('UpperBytesMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b'abcdefghijklmnopqrstuvwxyz'
        invokes.append(runner.call_contract(path, 'main', bytes_value, expected_result_type=bytes))
        expected_results.append(bytes_value.upper())

        bytes_value = b'a1b123y3z'
        invokes.append(runner.call_contract(path, 'main', bytes_value, expected_result_type=bytes))
        expected_results.append(bytes_value.upper())

        bytes_value = b'!@#$%123*-/'
        invokes.append(runner.call_contract(path, 'main', bytes_value, expected_result_type=bytes))
        expected_results.append(bytes_value.upper())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_lower(self):
        path, _ = self.get_deploy_file_paths('LowerBytesMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        invokes.append(runner.call_contract(path, 'main', bytes_value, expected_result_type=bytes))
        expected_results.append(bytes_value.lower())

        bytes_value = b'A1B123Y3Z'
        invokes.append(runner.call_contract(path, 'main', bytes_value, expected_result_type=bytes))
        expected_results.append(bytes_value.lower())

        bytes_value = b'!@#$%123*-/'
        invokes.append(runner.call_contract(path, 'main', bytes_value, expected_result_type=bytes))
        expected_results.append(bytes_value.lower())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_startswith_method(self):
        path, _ = self.get_deploy_file_paths('StartswithBytesMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        start = 0
        end = len(bytes_value)
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start, end))
        expected_results.append(bytes_value.startswith(subbytes_value, start, end))

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        start = 2
        end = 6
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start, end))
        expected_results.append(bytes_value.startswith(subbytes_value, start, end))

        bytes_value = b'unit_test'
        subbytes_value = b'it'
        start = 2
        end = 6
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start, end))
        expected_results.append(bytes_value.startswith(subbytes_value, start, end))

        bytes_value = b'unit_test'
        subbytes_value = b'it'
        start = 2
        end = 3
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start, end))
        expected_results.append(bytes_value.startswith(subbytes_value, start, end))

        bytes_value = b'unit_test'
        subbytes_value = b'unit_tes'
        start = -99
        end = -1
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start, end))
        expected_results.append(bytes_value.startswith(subbytes_value, start, end))

        bytes_value = b'unit_test'
        subbytes_value = b''
        start = 0
        end = 0
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start, end))
        expected_results.append(bytes_value.startswith(subbytes_value, start, end))

        bytes_value = b'unit_test'
        subbytes_value = b'unit_test'
        start = 0
        end = 99
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start, end))
        expected_results.append(bytes_value.startswith(subbytes_value, start, end))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_startswith_method_default_end(self):
        path, _ = self.get_deploy_file_paths('StartswithBytesMethodDefaultEnd.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        start = 0
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start))
        expected_results.append(bytes_value.startswith(subbytes_value, start))

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        start = 2
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start))
        expected_results.append(bytes_value.startswith(subbytes_value, start))

        bytes_value = b'unit_test'
        subbytes_value = b'it'
        start = 2
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start))
        expected_results.append(bytes_value.startswith(subbytes_value, start))

        bytes_value = b'unit_test'
        subbytes_value = b'it'
        start = 3
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start))
        expected_results.append(bytes_value.startswith(subbytes_value, start))

        bytes_value = b'unit_test'
        subbytes_value = b'unit_tes'
        start = -99
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start))
        expected_results.append(bytes_value.startswith(subbytes_value, start))

        bytes_value = b'unit_test'
        subbytes_value = b''
        start = 0
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start))
        expected_results.append(bytes_value.startswith(subbytes_value, start))

        bytes_value = b'unit_test'
        subbytes_value = b''
        start = 99
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start))
        expected_results.append(bytes_value.startswith(subbytes_value, start))

        bytes_value = b'unit_test'
        subbytes_value = b'unit_test'
        start = 0
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value, start))
        expected_results.append(bytes_value.startswith(subbytes_value, start))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_startswith_method_defaults(self):
        path, _ = self.get_deploy_file_paths('StartswithBytesMethodDefaults.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b'unit_test'
        subbytes_value = b'unit'
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value))
        expected_results.append(bytes_value.startswith(subbytes_value))

        bytes_value = b'unit_test'
        subbytes_value = b'unit_test'
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value))
        expected_results.append(bytes_value.startswith(subbytes_value))

        bytes_value = b'unit_test'
        subbytes_value = b''
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value))
        expected_results.append(bytes_value.startswith(subbytes_value))

        bytes_value = b'unit_test'
        subbytes_value = b'12345'
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value))
        expected_results.append(bytes_value.startswith(subbytes_value))

        bytes_value = b'unit_test'
        subbytes_value = b'bigger subbytes_value'
        invokes.append(runner.call_contract(path, 'main', bytes_value, subbytes_value))
        expected_results.append(bytes_value.startswith(subbytes_value))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_strip(self):
        path, _ = self.get_deploy_file_paths('StripBytesMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b'abcdefghijklmnopqrstuvwxyz'
        sub_bytes = b'abcxyz'
        invokes.append(runner.call_contract(path, 'main', bytes_value, sub_bytes,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.strip(sub_bytes))

        bytes_value = b'abcdefghijklmnopqrsvwxyz unit test abcdefghijklmnopqrsvwxyz'
        sub_bytes = b'abcdefghijklmnopqrsvwxyz '
        invokes.append(runner.call_contract(path, 'main', bytes_value, sub_bytes,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.strip(sub_bytes))

        bytes_value = b'0123456789hello world987654310'
        sub_bytes = b'0987654321'
        invokes.append(runner.call_contract(path, 'main', bytes_value, sub_bytes,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.strip(sub_bytes))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_strip_default(self):
        path, _ = self.get_deploy_file_paths('StripBytesMethodDefault.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b'     unit test    '
        invokes.append(runner.call_contract(path, 'main', bytes_value,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.strip())

        bytes_value = b'unit test    '
        invokes.append(runner.call_contract(path, 'main', bytes_value,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.strip())

        bytes_value = b'    unit test'
        invokes.append(runner.call_contract(path, 'main', bytes_value,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.strip())

        bytes_value = b' \t\n\r\f\vunit test \t\n\r\f\v'
        invokes.append(runner.call_contract(path, 'main', bytes_value,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.strip())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isdigit_method(self):
        path, _ = self.get_deploy_file_paths('IsdigitMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b'0123456789'
        invokes.append(runner.call_contract(path, 'main', bytes_value))
        expected_results.append(bytes_value.isdigit())

        bytes_value = b'23mixed01'
        invokes.append(runner.call_contract(path, 'main', bytes_value))
        expected_results.append(bytes_value.isdigit())

        bytes_value = b'no digits here'
        invokes.append(runner.call_contract(path, 'main', bytes_value))
        expected_results.append(bytes_value.isdigit())

        bytes_value = b''
        invokes.append(runner.call_contract(path, 'main', bytes_value))
        expected_results.append(bytes_value.isdigit())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_join_with_sequence(self):
        path, _ = self.get_deploy_file_paths('JoinBytesMethodWithSequence.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b' '
        sequence = [b"Unit", b"Test", b"Neo3-boa"]
        invokes.append(runner.call_contract(path, 'main', bytes_value, sequence,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.join(sequence))

        bytes_value = b' '
        sequence = []
        invokes.append(runner.call_contract(path, 'main', bytes_value, sequence,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.join(sequence))

        bytes_value = b' '
        sequence = [b"UnitTest"]
        invokes.append(runner.call_contract(path, 'main', bytes_value, sequence,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.join(sequence))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_join_with_dictionary(self):
        path, _ = self.get_deploy_file_paths('JoinBytesMethodWithDictionary.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b' '
        dictionary = {b"Unit": 1, b"Test": 2, b"Neo3-boa": 3}
        invokes.append(runner.call_contract(path, 'main', bytes_value, dictionary,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.join(dictionary))

        bytes_value = b' '
        dictionary = {}
        invokes.append(runner.call_contract(path, 'main', bytes_value, dictionary,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.join(dictionary))

        bytes_value = b' '
        dictionary = {b"UnitTest": 1}
        invokes.append(runner.call_contract(path, 'main', bytes_value, dictionary,
                                            expected_result_type=bytes))
        expected_results.append(bytes_value.join(dictionary))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_index(self):
        path, _ = self.get_deploy_file_paths('IndexBytes.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_ = b'unit test'
        subsequence = b'i'
        start = 0
        end = 4
        invokes.append(runner.call_contract(path, 'main', bytes_, subsequence, start, end))
        expected_results.append(bytes_.index(subsequence, start, end))

        bytes_ = b'unit test'
        bytes_sequence = b'i'
        start = 2
        end = 4
        invokes.append(runner.call_contract(path, 'main', bytes_, bytes_sequence, start, end))
        expected_results.append(bytes_.index(bytes_sequence, start, end))

        bytes_ = b'unit test'
        bytes_sequence = b'i'
        start = 0
        end = -1
        invokes.append(runner.call_contract(path, 'main', bytes_, bytes_sequence, start, end))
        expected_results.append(bytes_.index(bytes_sequence, start, end))

        bytes_ = b'unit test'
        bytes_sequence = b'n'
        start = 0
        end = 99
        invokes.append(runner.call_contract(path, 'main', bytes_, bytes_sequence, start, end))
        expected_results.append(bytes_.index(bytes_sequence, start, end))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invokes.append(runner.call_contract(path, 'main', 'unit test', 'i', 3, 4))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{self.SUBSEQUENCE_NOT_FOUND_MSG}$')

        invokes.append(runner.call_contract(path, 'main', 'unit test', 'i', 4, -1))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{self.SUBSEQUENCE_NOT_FOUND_MSG}$')

        invokes.append(runner.call_contract(path, 'main', 'unit test', 'i', 0, -99))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{self.SUBSEQUENCE_NOT_FOUND_MSG}$')

    def test_bytes_index_end_default(self):
        path, _ = self.get_deploy_file_paths('IndexBytesEndDefault.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_ = b'unit test'
        bytes_sequence = b't'
        start = 0
        invokes.append(runner.call_contract(path, 'main', bytes_, bytes_sequence, start))
        expected_results.append(bytes_.index(bytes_sequence, start))

        bytes_ = b'unit test'
        bytes_sequence = b't'
        start = 4
        invokes.append(runner.call_contract(path, 'main', bytes_, bytes_sequence, start))
        expected_results.append(bytes_.index(bytes_sequence, start))

        bytes_ = b'unit test'
        bytes_sequence = b't'
        start = 6
        invokes.append(runner.call_contract(path, 'main', bytes_, bytes_sequence, start))
        expected_results.append(bytes_.index(bytes_sequence, start))

        bytes_ = b'unit test'
        bytes_sequence = b'i'
        start = -10
        invokes.append(runner.call_contract(path, 'main', bytes_, bytes_sequence, start))
        expected_results.append(bytes_.index(bytes_sequence, start))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        bytes_ = b'unit test'
        bytes_sequence = b'i'
        start = 99
        invokes.append(runner.call_contract(path, 'main', bytes_, bytes_sequence, start))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{self.SUBSEQUENCE_NOT_FOUND_MSG}$')
        self.assertRaises(ValueError, bytes_.index, bytes_sequence, start)

        bytes_ = b'unit test'
        bytes_sequence = b's'
        start = -1
        invokes.append(runner.call_contract(path, 'main', bytes_, bytes_sequence, start))
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'{self.SUBSEQUENCE_NOT_FOUND_MSG}$')
        self.assertRaises(ValueError, bytes_.index, bytes_sequence, start)

    def test_bytes_index_defaults(self):
        path, _ = self.get_deploy_file_paths('IndexBytesDefaults.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_ = b'unit test'
        bytes_sequence = b'u'
        invokes.append(runner.call_contract(path, 'main', bytes_, bytes_sequence))
        expected_results.append(bytes_.index(bytes_sequence))

        bytes_ = b'unit test'
        bytes_sequence = b't'
        invokes.append(runner.call_contract(path, 'main', bytes_, bytes_sequence))
        expected_results.append(bytes_.index(bytes_sequence))

        bytes_ = b'unit test'
        bytes_sequence = b' '
        invokes.append(runner.call_contract(path, 'main', bytes_, bytes_sequence))
        expected_results.append(bytes_.index(bytes_sequence))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bytes_index_mismatched_type(self):
        path = self.get_contract_path('IndexBytesMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bytes_property_slicing(self):
        path, _ = self.get_deploy_file_paths('BytesPropertySlicing.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b'unit test'
        start = 0
        end = len(bytes_value)
        invokes.append(runner.call_contract(path, 'main', bytes_value, start, end, expected_result_type=bytes))
        expected_results.append(bytes_value[start:end])

        start = 2
        end = len(bytes_value) - 1
        invokes.append(runner.call_contract(path, 'main', bytes_value, start, end, expected_result_type=bytes))
        expected_results.append(bytes_value[start:end])

        start = len(bytes_value)
        end = 0
        invokes.append(runner.call_contract(path, 'main', bytes_value, start, end, expected_result_type=bytes))
        expected_results.append(bytes_value[start:end])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result, msg=x)

    def test_bytes_instance_variable_slicing(self):
        path, _ = self.get_deploy_file_paths('BytesInstanceVariableSlicing.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b'unit test'
        start = 0
        end = len(bytes_value)
        invokes.append(runner.call_contract(path, 'main', bytes_value, start, end, expected_result_type=bytes))
        expected_results.append(bytes_value[start:end])

        start = 2
        end = len(bytes_value) - 1
        invokes.append(runner.call_contract(path, 'main', bytes_value, start, end, expected_result_type=bytes))
        expected_results.append(bytes_value[start:end])

        start = len(bytes_value)
        end = 0
        invokes.append(runner.call_contract(path, 'main', bytes_value, start, end, expected_result_type=bytes))
        expected_results.append(bytes_value[start:end])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result, msg=x)

    def test_bytes_class_variable_slicing(self):
        path, _ = self.get_deploy_file_paths('BytesClassVariableSlicing.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        bytes_value = b'unit test'
        start = 0
        end = len(bytes_value)
        invokes.append(runner.call_contract(path, 'main', start, end, expected_result_type=bytes))
        expected_results.append(bytes_value[start:end])

        start = 2
        end = len(bytes_value) - 1
        invokes.append(runner.call_contract(path, 'main', start, end, expected_result_type=bytes))
        expected_results.append(bytes_value[start:end])

        start = len(bytes_value)
        end = 0
        invokes.append(runner.call_contract(path, 'main', start, end, expected_result_type=bytes))
        expected_results.append(bytes_value[start:end])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result, msg=x)

    def test_bytes_replace(self):
        path, _ = self.get_deploy_file_paths('ReplaceBytesMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        string = b'banana'
        old = b'an'
        new = b'o'
        count = -1
        invokes.append(runner.call_contract(path, 'main', string, old, new, count, expected_result_type=bytes))
        expected_results.append(string.replace(old, new, count))

        old = b'a'
        new = b'o'
        count = -1
        invokes.append(runner.call_contract(path, 'main', string, old, new, count, expected_result_type=bytes))
        expected_results.append(string.replace(old, new, count))

        old = b'a'
        new = b'oo'
        count = -1
        invokes.append(runner.call_contract(path, 'main', string, old, new, count, expected_result_type=bytes))
        expected_results.append(string.replace(old, new, count))

        string = b'banana'
        old = b'an'
        new = b'o'
        count = 1
        invokes.append(runner.call_contract(path, 'main', string, old, new, count, expected_result_type=bytes))
        expected_results.append(string.replace(old, new, count))

        string = b'banana'
        old = b'an'
        new = b'o'
        count = 2
        invokes.append(runner.call_contract(path, 'main', string, old, new, count, expected_result_type=bytes))
        expected_results.append(string.replace(old, new, count))

        string = b'banana'
        old = b'an'
        new = b'o'
        count = 3
        invokes.append(runner.call_contract(path, 'main', string, old, new, count, expected_result_type=bytes))
        expected_results.append(string.replace(old, new, count))

        string = b'banana'
        old = b'an'
        new = b'o'
        invokes.append(runner.call_contract(path, 'main_default_count', string, old, new, expected_result_type=bytes))
        expected_results.append(string.replace(old, new))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result, msg=x)

    def test_bytes_replace_mismatched_type(self):
        path = self.get_contract_path('ReplaceBytesMethodMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_bytes_replace_too_many_arguments(self):
        path = self.get_contract_path('ReplaceBytesMethodTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_bytes_replace_too_few_arguments(self):
        path = self.get_contract_path('ReplaceBytesMethodTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)