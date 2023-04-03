import unittest

from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.model.type.type import Type
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner


class TestBuiltinMethod(BoaTest):
    default_folder: str = 'test_sc/built_in_methods_test'

    # region len test

    def test_len_of_tuple(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH3      # a = (1, 2, 3)
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = len(a)
            + Opcode.SIZE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        path = self.get_contract_path('LenTuple.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_len_of_list(self):
        expected_output = (
            Opcode.INITSLOT
            + b'\x02'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3      # array length
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # b = len(a)
            + Opcode.SIZE
            + Opcode.STLOC1
            + Opcode.LDLOC1     # return b
            + Opcode.RET
        )
        path = self.get_contract_path('LenList.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_len_of_str(self):
        input = 'just a test'
        byte_input = String(input).to_bytes()
        expected_output = (
            Opcode.INITSLOT
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1            # push the bytes
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.PUSHDATA1            # push the bytes
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.SIZE
            + Opcode.RET
        )
        path = self.get_contract_path('LenString.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(11)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_len_of_bytes(self):
        path, _ = self.get_deploy_file_paths('LenBytes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(3)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_len_of_no_collection(self):
        path = self.get_contract_path('LenMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_len_too_many_parameters(self):
        path = self.get_contract_path('LenTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_len_too_few_parameters(self):
        path = self.get_contract_path('LenTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    # endregion

    # region append test

    def test_append_tuple(self):
        path = self.get_contract_path('AppendTuple.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_append_sequence(self):
        path = self.get_contract_path('AppendSequence.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_append_mutable_sequence(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # a.append(4)
            + Opcode.PUSH4
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.JMP
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        path = self.get_contract_path('AppendMutableSequence.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'append_example'))
        expected_results.append([1, 2, 3, 4])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_append_mutable_sequence_with_builtin(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # a.append(4)
            + Opcode.PUSH4
            + Opcode.OVER
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.CAT
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.APPEND
            + Opcode.JMP
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        path = self.get_contract_path('AppendMutableSequenceBuiltinCall.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'append_example'))
        expected_results.append([1, 2, 3, 4])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_append_too_many_parameters(self):
        path = self.get_contract_path('AppendTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_append_too_few_parameters(self):
        path = self.get_contract_path('AppendTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    # endregion

    # region clear test

    def test_clear_tuple(self):
        path = self.get_contract_path('ClearTuple.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_clear_mutable_sequence(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # a.clear()
            + Opcode.DUP
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(9).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSHDATA1
            + Integer(0).to_byte_array(min_length=1)
            + Opcode.CONVERT
            + Type.bytearray.stack_item
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.CLEARITEMS
            + Opcode.JMP
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        path = self.get_contract_path('ClearMutableSequence.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'clear_example'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_clear_mutable_sequence_with_builtin(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # MutableSequence.clear(a)
            + Opcode.DUP
            + Opcode.ISTYPE
            + Type.bytearray.stack_item
            + Opcode.JMPIFNOT
            + Integer(9).to_byte_array(min_length=1)
            + Opcode.DROP
            + Opcode.PUSHDATA1
            + Integer(0).to_byte_array(min_length=1)
            + Opcode.CONVERT
            + Type.bytearray.stack_item
            + Opcode.JMP
            + Integer(5).to_byte_array(min_length=1)
            + Opcode.CLEARITEMS
            + Opcode.JMP
            + Integer(3).to_byte_array(min_length=1)
            + Opcode.STLOC0
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        path = self.get_contract_path('ClearMutableSequenceBuiltinCall.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'clear_example'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_clear_too_many_parameters(self):
        path = self.get_contract_path('ClearTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_clear_too_few_parameters(self):
        path = self.get_contract_path('ClearTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    # endregion

    # region reverse test

    def test_reverse_tuple(self):
        path = self.get_contract_path('ReverseTuple.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_reverse_mutable_sequence(self):
        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSH3      # a = [1, 2, 3]
            + Opcode.PUSH2
            + Opcode.PUSH1
            + Opcode.PUSH3
            + Opcode.PACK
            + Opcode.STLOC0
            + Opcode.LDLOC0     # a.reverse()
            + Opcode.REVERSEITEMS
            + Opcode.LDLOC0     # return a
            + Opcode.RET
        )
        path = self.get_contract_path('ReverseMutableSequence.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([3, 2, 1])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_reverse_mutable_sequence_with_builtin(self):
        path, _ = self.get_deploy_file_paths('ReverseMutableSequenceBuiltinCall.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(b'\x03\x02\x01')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_reverse_too_many_parameters(self):
        path = self.get_contract_path('ReverseTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_reverse_too_few_parameters(self):
        path = self.get_contract_path('ReverseTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    # endregion

    # region extend test

    def test_extend_tuple(self):
        path = self.get_contract_path('ExtendTuple.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_extend_sequence(self):
        path = self.get_contract_path('ExtendSequence.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_extend_mutable_sequence(self):
        path, _ = self.get_deploy_file_paths('ExtendMutableSequence.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 2, 3, 4, 5, 6])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_extend_mutable_sequence_with_builtin(self):
        path, _ = self.get_deploy_file_paths('ExtendMutableSequenceBuiltinCall.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append([1, 2, 3, 4, 5, 6])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_extend_too_many_parameters(self):
        path = self.get_contract_path('ExtendTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_extend_too_few_parameters(self):
        path = self.get_contract_path('ExtendTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    # endregion

    # region to_script_hash test

    def test_script_hash_int(self):
        path, _ = self.get_deploy_file_paths('ScriptHashInt.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from boa3.internal.neo import to_script_hash
        script_hash = to_script_hash(Integer(123).to_byte_array())

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_script_hash_int_with_builtin(self):
        path, _ = self.get_deploy_file_paths('ScriptHashIntBuiltinCall.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from boa3.internal.neo import to_script_hash
        script_hash = to_script_hash(Integer(123).to_byte_array())

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_script_hash_str(self):
        path, _ = self.get_deploy_file_paths('ScriptHashStr.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from boa3.internal.neo import to_script_hash
        expected_result = to_script_hash(String('NUnLWXALK2G6gYa7RadPLRiQYunZHnncxg').to_bytes())
        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        expected_result = to_script_hash(String('123').to_bytes())
        invokes.append(runner.call_contract(path, 'Main2',
                                            expected_result_type=bytes))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_script_hash_str_with_builtin(self):
        path, _ = self.get_deploy_file_paths('ScriptHashStrBuiltinCall.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from boa3.internal.neo import to_script_hash
        script_hash = to_script_hash(String('123').to_bytes())

        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_script_hash_variable(self):
        path, _ = self.get_deploy_file_paths('ScriptHashVariable.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from boa3.internal.neo import to_script_hash
        from base58 import b58encode
        value = b58encode(Integer(123).to_byte_array())
        if isinstance(value, int):
            value = Integer(value).to_byte_array()

        script_hash = to_script_hash(value)

        invokes.append(runner.call_contract(path, 'Main', value,
                                            expected_result_type=bytes))
        expected_results.append(script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', 123)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)

    def test_script_hash_variable_with_builtin(self):
        path, _ = self.get_deploy_file_paths('ScriptHashVariableBuiltinCall.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        from boa3.internal.neo import to_script_hash
        from base58 import b58encode

        script_hash = to_script_hash(String('123').to_bytes())
        invokes.append(runner.call_contract(path, 'Main', '123',
                                            expected_result_type=bytes))
        expected_results.append(script_hash)

        value = b58encode('123')
        if isinstance(value, int):
            value = Integer(value).to_byte_array()

        script_hash = to_script_hash(value)
        invokes.append(runner.call_contract(path, 'Main', value,
                                            expected_result_type=bytes))
        expected_results.append(script_hash)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_script_hash_too_many_parameters(self):
        path = self.get_contract_path('ScriptHashTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_script_hash_too_few_parameters(self):
        path = self.get_contract_path('ScriptHashTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_script_hash_mismatched_types(self):
        path = self.get_contract_path('ScriptHashMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_script_hash_builtin_mismatched_types(self):
        path = self.get_contract_path('ScriptHashBuiltinMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region to_bytes test

    def test_int_to_bytes(self):
        path, _ = self.get_deploy_file_paths('IntToBytes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = Integer(123).to_byte_array()
        invokes.append(runner.call_contract(path, 'int_to_bytes',
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_int_zero_to_bytes(self):
        path, _ = self.get_deploy_file_paths('IntZeroToBytes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = Integer(0).to_byte_array(min_length=1)
        invokes.append(runner.call_contract(path, 'int_to_bytes',
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_int_to_bytes_with_builtin(self):
        path, _ = self.get_deploy_file_paths('IntToBytesWithBuiltin.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = Integer(123).to_byte_array()
        invokes.append(runner.call_contract(path, 'int_to_bytes',
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_int_to_bytes_as_parameter(self):
        path, _ = self.get_deploy_file_paths('IntToBytesAsParameter.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'int_to_bytes', 1111,
                                            expected_result_type=bytes))
        # return is Void, checking to see if there is no error
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_to_bytes(self):
        value = String('123').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1        # '123'.to_bytes()
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
            + Opcode.RET
        )

        path = self.get_contract_path('StrToBytes.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'str_to_bytes',
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_to_bytes_with_builtin(self):
        value = String('123').to_bytes()
        expected_output = (
            Opcode.PUSHDATA1        # str.to_bytes('123')
            + Integer(len(value)).to_byte_array(min_length=1)
            + value
            + Opcode.RET
        )

        path = self.get_contract_path('StrToBytesWithBuiltin.py')
        output = self.compile(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'str_to_bytes',
                                            expected_result_type=bytes))
        expected_results.append(value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_to_bytes_mismatched_types(self):
        path = self.get_contract_path('ToBytesMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region print test

    def test_print_int(self):
        path, _ = self.get_deploy_file_paths('PrintInt.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invoke_logs = runner.get_logs()
        self.assertEqual(1, len(invoke_logs))
        self.assertEqual('42', invoke_logs[0].message)

    def test_print_str(self):
        path, _ = self.get_deploy_file_paths('PrintStr.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invoke_logs = runner.get_logs()
        self.assertEqual(1, len(invoke_logs))
        self.assertEqual('str', invoke_logs[0].message)

    def test_print_bytes(self):
        path, _ = self.get_deploy_file_paths('PrintBytes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invoke_logs = runner.get_logs()
        self.assertEqual(1, len(invoke_logs))
        self.assertEqual('\x01\x02\x03', invoke_logs[0].message)

    def test_print_bool(self):
        path, _ = self.get_deploy_file_paths('PrintBool.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invoke_logs = runner.get_logs()
        self.assertEqual(1, len(invoke_logs))
        self.assertEqual('true', invoke_logs[0].message)

    def test_print_list(self):
        path, _ = self.get_deploy_file_paths('PrintList.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        import json
        expected_print = json.dumps([1, 2, 3, 4], separators=(',', ':'))

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invoke_logs = runner.get_logs()
        self.assertEqual(1, len(invoke_logs))
        self.assertEqual(expected_print, invoke_logs[0].message)

    def test_print_user_class(self):
        path, _ = self.get_deploy_file_paths('PrintClass.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        import json
        expected_print = json.dumps({
            'val1': 1,
            'val2': 2
        }, separators=(',', ':'))

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invoke_logs = runner.get_logs()
        self.assertEqual(1, len(invoke_logs))
        self.assertEqual(expected_print, invoke_logs[0].message)

    def test_print_many_values(self):
        path, _ = self.get_deploy_file_paths('PrintManyValues.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invoke_logs = runner.get_logs()
        self.assertEqual(4, len(invoke_logs))
        for index in range(4):
            self.assertEqual(str(index + 1), invoke_logs[index].message)

    def test_print_no_args(self):
        path, _ = self.get_deploy_file_paths('PrintNoArgs.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(None)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        invoke_logs = runner.get_logs()
        self.assertEqual(0, len(invoke_logs))

    def test_print_missing_outer_function_return(self):
        path = self.get_contract_path('PrintIntMissingFunctionReturn.py')
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, path)

    # endregion

    # region isinstance test

    def test_isinstance_int_literal(self):
        path, _ = self.get_deploy_file_paths('IsInstanceIntLiteral.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_int_variable(self):
        path, _ = self.get_deploy_file_paths('IsInstanceIntVariable.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', 'string'))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_bool_literal(self):
        path, _ = self.get_deploy_file_paths('IsInstanceBoolLiteral.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_bool_variable(self):
        path, _ = self.get_deploy_file_paths('IsInstanceBoolVariable.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'Main', 'string'))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_str_literal(self):
        path, _ = self.get_deploy_file_paths('IsInstanceStrLiteral.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_str_variable(self):
        path, _ = self.get_deploy_file_paths('IsInstanceStrVariable.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', 'string'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_list_literal(self):
        path, _ = self.get_deploy_file_paths('IsInstanceListLiteral.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_tuple_literal(self):
        path, _ = self.get_deploy_file_paths('IsInstanceTupleLiteral.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_tuple_variable(self):
        path, _ = self.get_deploy_file_paths('IsInstanceTupleVariable.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', 'string'))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', []))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_many_types(self):
        path, _ = self.get_deploy_file_paths('IsInstanceManyTypes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 10))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'Main', False))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'Main', 'string'))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', {}))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_many_types_with_class(self):
        path, _ = self.get_deploy_file_paths('IsInstanceManyTypesWithClass.py')

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 42))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'Main', bytes(10)))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', []))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'Main', 'some string'))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', bytes(20)))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'Main', None))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', {1: 2, 2: 4}))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_uint160(self):
        path, _ = self.get_deploy_file_paths('IsInstanceUInt160.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', bytes(10)))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', bytes(20)))
        expected_results.append(True)

        invokes.append(runner.call_contract(path, 'Main', bytes(30)))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'Main', 42))
        expected_results.append(False)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isinstance_uint256(self):
        path, _ = self.get_deploy_file_paths('IsInstanceUInt256.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', bytes(10)))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', bytes(20)))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', bytes(30)))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', bytes(32)))
        expected_results.append(True)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region exit test

    def test_exit(self):
        path, _ = self.get_deploy_file_paths('Exit.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', False))
        expected_results.append(123)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', True)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, self.ABORTED_CONTRACT_MSG)

    # endregion

    # region max test

    def test_max_int(self):
        path, _ = self.get_deploy_file_paths('MaxInt.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value1 = 10
        value2 = 999
        expected_result = max(value1, value2)
        invokes.append(runner.call_contract(path, 'main', value1, value2))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_max_int_more_arguments(self):
        path, _ = self.get_deploy_file_paths('MaxIntMoreArguments.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        numbers = 4, 1, 16, 8, 2
        expected_result = max(numbers)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_max_str(self):
        path, _ = self.get_deploy_file_paths('MaxStr.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value1 = 'foo'
        value2 = 'bar'
        expected_result = max(value1, value2)
        invokes.append(runner.call_contract(path, 'main', value1, value2))
        expected_results.append(expected_result)

        invokes.append(runner.call_contract(path, 'main', value2, value1))
        expected_results.append(expected_result)

        value1 = 'alg'
        value2 = 'al'
        expected_result = max(value1, value2)
        invokes.append(runner.call_contract(path, 'main', value1, value2))
        expected_results.append(expected_result)

        value = 'some string'
        expected_result = max(value, value)
        invokes.append(runner.call_contract(path, 'main', value, value))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_max_str_more_arguments(self):
        path, _ = self.get_deploy_file_paths('MaxStrMoreArguments.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        values = 'Lorem', 'ipsum', 'dolor', 'sit', 'amet'
        expected_result = max(values)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_max_bytes(self):
        path, _ = self.get_deploy_file_paths('MaxBytes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value1 = b'foo'
        value2 = b'bar'
        expected_result = max(value1, value2)
        invokes.append(runner.call_contract(path, 'main', value1, value2, expected_result_type=bytes))
        expected_results.append(expected_result)

        invokes.append(runner.call_contract(path, 'main', value2, value1, expected_result_type=bytes))
        expected_results.append(expected_result)

        value1 = b'alg'
        value2 = b'al'
        expected_result = max(value1, value2)
        invokes.append(runner.call_contract(path, 'main', value1, value2, expected_result_type=bytes))
        expected_results.append(expected_result)

        value = b'some string'
        expected_result = max(value, value)
        invokes.append(runner.call_contract(path, 'main', value, value, expected_result_type=bytes))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_max_bytes_more_arguments(self):
        path, _ = self.get_deploy_file_paths('MaxBytesMoreArguments.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        values = b'Lorem', b'ipsum', b'dolor', b'sit', b'amet'
        expected_result = max(values)
        invokes.append(runner.call_contract(path, 'main', expected_result_type=bytes))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_max_too_few_parameters(self):
        path = self.get_contract_path('MaxTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_max_mismatched_types(self):
        path = self.get_contract_path('MaxMismatchedTypes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region min test

    def test_min_int(self):
        path, _ = self.get_deploy_file_paths('MinInt.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val1 = 50
        val2 = 1
        expected_result = min(val1, val2)
        invokes.append(runner.call_contract(path, 'main', val1, val2))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_min_int_more_arguments(self):
        path, _ = self.get_deploy_file_paths('MinIntMoreArguments.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        numbers = 2, 8, 1, 4, 16
        expected_result = min(numbers)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_min_str(self):
        path, _ = self.get_deploy_file_paths('MinStr.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value1 = 'foo'
        value2 = 'bar'
        expected_result = min(value1, value2)
        invokes.append(runner.call_contract(path, 'main', value1, value2))
        expected_results.append(expected_result)

        invokes.append(runner.call_contract(path, 'main', value2, value1))
        expected_results.append(expected_result)

        value1 = 'alg'
        value2 = 'al'
        expected_result = min(value1, value2)
        invokes.append(runner.call_contract(path, 'main', value1, value2))
        expected_results.append(expected_result)

        value = 'some string'
        expected_result = min(value, value)
        invokes.append(runner.call_contract(path, 'main', value, value))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_min_str_more_arguments(self):
        path, _ = self.get_deploy_file_paths('MinStrMoreArguments.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        values = 'Lorem', 'ipsum', 'dolor', 'sit', 'amet'
        expected_result = min(values)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_min_bytes(self):
        path, _ = self.get_deploy_file_paths('MinBytes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value1 = b'foo'
        value2 = b'bar'
        expected_result = min(value1, value2)
        invokes.append(runner.call_contract(path, 'main', value1, value2, expected_result_type=bytes))
        expected_results.append(expected_result)

        invokes.append(runner.call_contract(path, 'main', value2, value1, expected_result_type=bytes))
        expected_results.append(expected_result)

        value1 = b'alg'
        value2 = b'al'
        expected_result = min(value1, value2)
        invokes.append(runner.call_contract(path, 'main', value1, value2, expected_result_type=bytes))
        expected_results.append(expected_result)

        value = b'some string'
        expected_result = min(value, value)
        invokes.append(runner.call_contract(path, 'main', value, value, expected_result_type=bytes))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_min_bytes_more_arguments(self):
        path, _ = self.get_deploy_file_paths('MinBytesMoreArguments.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        values = b'Lorem', b'ipsum', b'dolor', b'sit', b'amet'
        expected_result = min(values)
        invokes.append(runner.call_contract(path, 'main', expected_result_type=bytes))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_min_too_few_parameters(self):
        path = self.get_contract_path('MinTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_min_mismatched_types(self):
        path = self.get_contract_path('MinMismatchedTypes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    # endregion

    # region abs test

    def test_abs(self):
        path, _ = self.get_deploy_file_paths('Abs.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = 10
        expected_result = abs(val)
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(expected_result)

        expected_result = abs(-1)
        invokes.append(runner.call_contract(path, 'main', -1))
        expected_results.append(expected_result)

        expected_result = abs(1)
        invokes.append(runner.call_contract(path, 'main', 1))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_abs_bytes(self):
        path = self.get_contract_path('AbsMismatchedTypesBytes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_abs_string(self):
        path = self.get_contract_path('AbsMismatchedTypesString.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_abs_too_few_parameters(self):
        path = self.get_contract_path('AbsTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_abs_too_many_parameters(self):
        path = self.get_contract_path('AbsTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    # endregion

    # region sum test

    def test_sum(self):
        path, _ = self.get_deploy_file_paths('Sum.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = [1, 2, 3, 4]
        expected_result = sum(val)
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(expected_result)

        val = list(range(10, 20, 2))
        expected_result = sum(val)
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_sum_with_start(self):
        path, _ = self.get_deploy_file_paths('SumWithStart.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = [1, 2, 3, 4]
        expected_result = sum(val, 10)
        invokes.append(runner.call_contract(path, 'main', val, 10))
        expected_results.append(expected_result)

        val = list(range(10, 20, 2))
        expected_result = sum(val, 20)
        invokes.append(runner.call_contract(path, 'main', val, 20))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_sum_mismatched_type(self):
        path = self.get_contract_path('SumMismatchedTypes.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_sum_too_few_parameters(self):
        path = self.get_contract_path('SumTooFewParameters.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_sum_too_many_parameters(self):
        path = self.get_contract_path('SumTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    # endregion

    # region str split test

    def test_str_split(self):
        path, _ = self.get_deploy_file_paths('StrSplit.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        string = '1#2#3#4'
        separator = '#'
        maxsplit = 2
        expected_result = string.split(separator, maxsplit)
        invokes.append(runner.call_contract(path, 'main', string, separator, maxsplit))
        expected_results.append(expected_result)

        string = '1#2#3#4'
        separator = '#'
        maxsplit = 1
        expected_result = string.split(separator, maxsplit)
        invokes.append(runner.call_contract(path, 'main', string, separator, maxsplit))
        expected_results.append(expected_result)

        string = '1#2#3#4'
        separator = '#'
        maxsplit = 0
        expected_result = string.split(separator, maxsplit)
        invokes.append(runner.call_contract(path, 'main', string, separator, maxsplit))
        expected_results.append(expected_result)

        string = 'unit123test123str123split'
        separator = '123'
        maxsplit = 1
        expected_result = string.split(separator, maxsplit)
        invokes.append(runner.call_contract(path, 'main', string, separator, maxsplit))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_split_maxsplit_default(self):
        path, _ = self.get_deploy_file_paths('StrSplitMaxsplitDefault.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        string = '1#2#3#4'
        separator = '#'
        expected_result = string.split(separator)
        invokes.append(runner.call_contract(path, 'main', string, separator))
        expected_results.append(expected_result)

        string = 'unit123test123str123split'
        separator = '123'
        expected_result = string.split(separator)
        invokes.append(runner.call_contract(path, 'main', string, separator))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_split_default(self):
        path, _ = self.get_deploy_file_paths('StrSplitSeparatorDefault.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        string = '1 2 3 4'
        expected_result = string.split()
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region count test

    def test_count_list_int(self):
        path, _ = self.get_deploy_file_paths('CountListInt.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = [1, 2, 3, 4, 1, 1, 0]
        expected_result = list_.count(1)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_list_str(self):
        path, _ = self.get_deploy_file_paths('CountListStr.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = ['unit', 'test', 'unit', 'unit', 'random', 'string']
        expected_result = list_.count('unit')
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_list_bytes(self):
        path, _ = self.get_deploy_file_paths('CountListBytes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = [b'unit', b'test', b'unit', b'unit', b'random', b'string']
        expected_result = list_.count(b'unit')
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_list_different_primitive_types(self):
        path, _ = self.get_deploy_file_paths('CountListDifferentPrimitiveTypes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = [b'unit', 'test', b'unit', b'unit', 123, 123, True, False]
        expected_result = list_.count(b'unit'), list_.count('test'), list_.count(123)
        invokes.append(runner.call_contract(path, 'main',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_list_different_any_types(self):
        path, _ = self.get_deploy_file_paths('CountListAnyType.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        mixed_list = [[b'unit', b'unit'], [123, 123], [True, False], [True, False], [b'unit', 'test'], 'not list']

        count1 = mixed_list.count([b'unit', 'test'])
        count2 = mixed_list.count([123, 123])
        count3 = mixed_list.count([True, False])
        count4 = mixed_list.count(['random value', 'random value', 'random value'])
        expected_result = [count1, count2, count3, count4]

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_list_only_sequences(self):
        path, _ = self.get_deploy_file_paths('CountListOnlySequences.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        mixed_list = [[b'unit', b'unit'], [123, 123], [True, False], [True, False], [b'unit', 'test']]

        count1 = mixed_list.count([b'unit', 'test'])
        count2 = mixed_list.count([123, 123])
        count3 = mixed_list.count([True, False])
        count4 = mixed_list.count(['random value', 'random value', 'random value'])
        expected_result = [count1, count2, count3, count4]

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_list_empty(self):
        path, _ = self.get_deploy_file_paths('CountListEmpty.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        list_ = []
        expected_result = list_.count(1)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_tuple_int(self):
        path, _ = self.get_deploy_file_paths('CountTupleInt.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        tuple_ = (1, 2, 3, 4, 1, 1, 0)
        expected_result = tuple_.count(1)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_tuple_str(self):
        path, _ = self.get_deploy_file_paths('CountTupleStr.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        tuple_ = ('unit', 'test', 'unit', 'unit', 'random', 'string')
        expected_result = tuple_.count('unit')
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_tuple_bytes(self):
        path, _ = self.get_deploy_file_paths('CountTupleBytes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        tuple_ = (b'unit', b'test', b'unit', b'unit', b'random', b'string')
        expected_result = tuple_.count(b'unit')
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_tuple_different_types(self):
        path, _ = self.get_deploy_file_paths('CountTupleDifferentTypes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        tuple_ = (b'unit', 'test', b'unit', b'unit', 123, 123, True, False)
        expected_result = tuple_.count(b'unit'), tuple_.count('test'), tuple_.count(123)
        invokes.append(runner.call_contract(path, 'main',
                                            expected_result_type=tuple))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_tuple_different_non_primitive_types(self):
        path, _ = self.get_deploy_file_paths('CountTupleDifferentNonPrimitiveTypes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        mixed_list = ([b'unit', 'test'], [b'unit', b'unit'], [123, 123], [True, False], [True, False])

        count1 = mixed_list.count([b'unit', 'test'])
        count2 = mixed_list.count([123, 123])
        count3 = mixed_list.count([True, False])
        expected_result = [count1, count2, count3]

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_tuple_empty(self):
        path, _ = self.get_deploy_file_paths('CountTupleEmpty.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        tuple_ = ()
        expected_result = tuple_.count(1)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_range(self):
        path, _ = self.get_deploy_file_paths('CountRange.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = range(10).count(1)
        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_sequence_too_many_parameters(self):
        path = self.get_contract_path('CountSequenceTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_count_sequence_too_few_parameters(self):
        path = self.get_contract_path('CountSequenceTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_count_str(self):
        path, _ = self.get_deploy_file_paths('CountStr.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 0
        end = 43
        expected_result = str_.count(substr, start, end)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start, end))
        expected_results.append(expected_result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 0
        end = 1000
        expected_result = str_.count(substr, start, end)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start, end))
        expected_results.append(expected_result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 0
        end = -1000
        expected_result = str_.count(substr, start, end)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start, end))
        expected_results.append(expected_result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 0
        end = -4
        expected_result = str_.count(substr, start, end)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start, end))
        expected_results.append(expected_result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 23
        end = 43
        expected_result = str_.count(substr, start, end)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start, end))
        expected_results.append(expected_result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = -11
        end = 43
        expected_result = str_.count(substr, start, end)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start, end))
        expected_results.append(expected_result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = -1000
        end = 43
        expected_result = str_.count(substr, start, end)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start, end))
        expected_results.append(expected_result)

        str_ = 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
        substr = 'e'
        start = 1000
        end = 43
        expected_result = str_.count(substr, start, end)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start, end))
        expected_results.append(expected_result)

        str_ = 'a string that will be used in the unit test'
        substr = 'string'
        start = 0
        end = 43
        expected_result = str_.count(substr, start, end)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start, end))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_str_end_default(self):
        path, _ = self.get_deploy_file_paths('CountStrEndDefault.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        str_ = 'a string that will be used in the unit test'
        substr = 'string'
        start = 0
        expected_result = str_.count(substr, start)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start))
        expected_results.append(expected_result)

        str_ = 'a string that will be used in the unit test'
        substr = 'string'
        start = 4
        expected_result = str_.count(substr, start)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start))
        expected_results.append(expected_result)

        str_ = 'eeeeeeeeeee'
        substr = 'e'
        start = 0
        expected_result = str_.count(substr, start)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start))
        expected_results.append(expected_result)

        str_ = 'eeeeeeeeeee'
        substr = 'e'
        start = 5
        expected_result = str_.count(substr, start)
        invokes.append(runner.call_contract(path, 'main', str_, substr, start))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_str_default(self):
        path, _ = self.get_deploy_file_paths('CountStrDefault.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        str_ = 'a string that will be used in the unit test'
        substr = 'string'
        expected_result = str_.count(substr)
        invokes.append(runner.call_contract(path, 'main', str_, substr))
        expected_results.append(expected_result)

        str_ = 'eeeeeeeeeee'
        substr = 'e'
        expected_result = str_.count(substr)
        invokes.append(runner.call_contract(path, 'main', str_, substr))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_count_str_too_many_parameters(self):
        path = self.get_contract_path('CountStrTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_count_str_too_few_parameters(self):
        path = self.get_contract_path('CountStrTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    # endregion

    # region super test

    def test_super_with_args(self):
        # TODO: Change when super with args is implemented
        path = self.get_contract_path('SuperWithArgs.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_super_call_method(self):
        path, _ = self.get_deploy_file_paths('SuperCallMethod.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        super_method_expected_result = -20
        arg = 20
        invokes.append(runner.call_contract(path, 'example_method', arg))
        expected_results.append(arg)

        arg = 30
        invokes.append(runner.call_contract(path, 'example_method', arg))
        expected_results.append(arg)

        arg = 40
        invokes.append(runner.call_contract(path, 'example_method', arg))
        expected_results.append(super_method_expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region int test

    # TODO: Int constructor is not accepting more than one method
    @unittest.skip('Int constructor is not accepting more than one method')
    def test_int_str(self):
        path = self.get_contract_path('IntStr.py')
        self.compile_and_save(path)  # it doesn't compile, it isn't implemented yet

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = '0b101'
        base = 0
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '0B101'
        base = 0
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '0b101'
        base = 2
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '0B101'
        base = 2
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '0o123'
        base = 0
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '0O123'
        base = 0
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '0o123'
        base = 8
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '0O123'
        base = 8
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '0x123'
        base = 0
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '0X123'
        base = 0
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '0x123'
        base = 16
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '0X123'
        base = 16
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '123'
        base = 16
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = '11'
        base = 11
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = 'abcdef'
        base = 16
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        value = 'abcdefg'
        base = 16
        runner.call_contract(path, 'main', value, base)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        with self.assertRaises(ValueError):
            int(value, base)

        value = '0x123'
        base = 8
        runner.call_contract(path, 'main', value, base)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        with self.assertRaises(ValueError):
            int(value, base)

    # TODO: Int constructor is not accepting more than one method
    @unittest.skip('Int constructor is not accepting more than one method')
    def test_int_bytes(self):
        path = self.get_contract_path('IntBytes.py')
        self.compile_and_save(path)  # it doesn't compile, it isn't implemented yet

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = b'0b101'
        base = 0
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'0B101'
        base = 0
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'0b101'
        base = 2
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'0B101'
        base = 2
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'0o123'
        base = 0
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'0O123'
        base = 0
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'0o123'
        base = 8
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'0O123'
        base = 8
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'0x123'
        base = 0
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'0X123'
        base = 0
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'0x123'
        base = 16
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'0X123'
        base = 16
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'123'
        base = 16
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'11'
        base = 11
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        value = b'abcdef'
        base = 16
        invokes.append(runner.call_contract(path, 'main', value, base))
        expected_results.append(int(value, base))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        value = b'abcdefg'
        base = 16
        runner.call_contract(path, 'main', value, base)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        with self.assertRaises(ValueError):
            int(value, base)

        value = b'0x123'
        base = 8
        runner.call_contract(path, 'main', value, base)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        with self.assertRaises(ValueError):
            int(value, base)

    def test_int_int(self):
        path, _ = self.get_deploy_file_paths('IntInt.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = 10
        invokes.append(runner.call_contract(path, 'main', value))
        expected_results.append(int(value))

        value = -10
        invokes.append(runner.call_contract(path, 'main', value))
        expected_results.append(int(value))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_int_int_too_many_parameters(self):
        path = self.get_contract_path('IntIntTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_int_no_parameters(self):
        path, _ = self.get_deploy_file_paths('IntNoParameters.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(int())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region bool test

    def test_bool(self):
        path, _ = self.get_deploy_file_paths('Bool.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = 1
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        val = 'test'
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        val = b'test'
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        val = [1, 2, 3]
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        val = {'1': 2}
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bool_bytes(self):
        path, _ = self.get_deploy_file_paths('BoolBytes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = b'123'
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        val = b''
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bool_class(self):
        path, _ = self.get_deploy_file_paths('BoolClass.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        # dunder methods are not supported in neo3-boa
        class Example:
            def __init__(self):
                self.test = 123

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(bool(Example()))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bool_dict(self):
        path, _ = self.get_deploy_file_paths('BoolDict.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = {}
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        val = {'a': 123, 'b': 56, 'c': 1}
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bool_int(self):
        path, _ = self.get_deploy_file_paths('BoolInt.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = -1
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        val = 0
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        val = 1
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bool_list(self):
        path, _ = self.get_deploy_file_paths('BoolList.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = []
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        val = [1, 2, 3, 4, 5]
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bool_range(self):
        path, _ = self.get_deploy_file_paths('BoolRange.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'range_0'))
        expected_results.append(bool(range(0)))

        invokes.append(runner.call_contract(path, 'range_not_0'))
        expected_results.append(bool(range(10)))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_bool_str(self):
        path, _ = self.get_deploy_file_paths('BoolStr.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = 'unit test'
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        val = ''
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(bool(val))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region list test

    def test_list_any(self):
        path, _ = self.get_deploy_file_paths('ListAny.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = [1, 2, 3, 4]
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(val))

        val = {'a': 1, 'b': '2', 'c': True, 'd': b'01', '12e12e12e12': 123}
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(val))

        val = 'unit test'
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(bytes(val, 'utf-8')))

        val = b'unit test'
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(val))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        val = 123
        runner.call_contract(path, 'main', val)
        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)

    def test_list_default(self):
        path, _ = self.get_deploy_file_paths('ListDefault.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append(list())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_sequence(self):
        path, _ = self.get_deploy_file_paths('ListSequence.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = [1, 2, 3, 4]
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(val))

        val = (1, 2, 3, 4)
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(val))

        val = range(0, 10)
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(val))

        val = [1, 2, 3, 4]
        invokes.append(runner.call_contract(path, 'verify_list_unchanged', val))
        new_list = list(val)
        val[0] = val[1]
        expected_results.append(new_list)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_sequence_mismatched_return_type(self):
        path = self.get_contract_path('ListSequenceMismatchedReturnType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_mapping(self):
        path, _ = self.get_deploy_file_paths('ListMapping.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = {'a': 1, 'b': 2, 'c': 3, 'd': 0, '12e12e12e12': 123}
        invokes.append(runner.call_contract(path, 'main', val))
        # result should be a list of all the keys used in the dictionary, in insertion order
        expected_results.append(list(val))

        val = {'a': 1, 'b': '2', 'c': True, 'd': b'01', '12e12e12e12': 123}
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(val))

        val = {1: 0, 23: 12, -10: 412, 25: '123'}
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(val))

        val = {b'123': 123, b'test': 'test', b'unit': 'unit'}
        expected_result = [String.from_bytes(item) for item in val]
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(expected_result)

        val = {'a': 1, 'b': '2', 'c': True, 1: 0, 23: 12, 25: 'value'}
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(val))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_mapping_mismatched_return_type(self):
        path = self.get_contract_path('ListMappingMismatchedReturnType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_bytes(self):
        path, _ = self.get_deploy_file_paths('ListBytes.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = b'unit test'
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(val))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_bytes_mismatched_return_type(self):
        path = self.get_contract_path('ListBytesMismatchedReturnType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_str(self):
        path, _ = self.get_deploy_file_paths('ListString.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        val = 'unit test'
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(val))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_list_str_mismatched_return_type(self):
        path = self.get_contract_path('ListStringMismatchedReturnType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_list_bytes_str(self):
        path, _ = self.get_deploy_file_paths('ListBytesString.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        # If the compiler doesn't have a type hint to know if it's a bytes or str value it will consider it as bytes
        val = 'unit test'
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(bytes(val, 'utf-8')))

        val = b'unit test'
        invokes.append(runner.call_contract(path, 'main', val))
        expected_results.append(list(val))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    # endregion

    # region str test

    def test_str_bytes_str(self):
        path, _ = self.get_deploy_file_paths('StrByteString.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = 'test'
        invokes.append(runner.call_contract(path, 'str_parameter', value))
        expected_results.append(str(value))

        value = b'test'
        invokes.append(runner.call_contract(path, 'bytes_parameter', value))
        # since bytes and string is the same thing internally it will return 'test' instead of the "b'test'"
        expected_results.append('test')

        invokes.append(runner.call_contract(path, 'empty_parameter'))
        expected_results.append(str())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_int(self):
        path, _ = self.get_deploy_file_paths('StrInt.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = 1234567890
        invokes.append(runner.call_contract(path, 'main', value))
        expected_results.append(str(value))

        value = -1234567890
        invokes.append(runner.call_contract(path, 'main', value))
        expected_results.append(str(value))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_bool(self):
        path, _ = self.get_deploy_file_paths('StrBool.py')
        runner = NeoTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        value = True
        invokes.append(runner.call_contract(path, 'main', value))
        expected_results.append(str(value))

        value = False
        invokes.append(runner.call_contract(path, 'main', value))
        expected_results.append(str(value))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_str_too_many_parameters(self):
        path = self.get_contract_path('StrTooManyParameters.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    # endregion
