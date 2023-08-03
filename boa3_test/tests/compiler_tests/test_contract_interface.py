from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestContractInterface(BoaTest):
    default_folder: str = 'test_sc/contract_interface_test'

    def test_contract_interface_decorator_literal_hash_str(self):
        path = self.get_contract_path('ContractInterfaceLiteralStrHash.py')
        self.compile(path)  # test if compiles because the smart contract doesn't exist

    def test_contract_interface_decorator_literal_hash_bytes(self):
        path = self.get_contract_path('ContractInterfaceLiteralBytesHash.py')
        self.compile(path)  # test if compiles because the smart contract doesn't exist

    def test_contract_interface_decorator_invalid_hash(self):
        path = self.get_contract_path('ContractInterfaceInvalidHash.py')
        self.assertCompilerLogs(CompilerError.InvalidUsage, path)

    def test_contract_interface_decorator_variable_hash(self):
        path = self.get_contract_path('ContractInterfaceVariableArgument.py')
        self.assertCompilerLogs(CompilerError.InvalidUsage, path)

    def test_contract_interface_decorator_too_few_arguments(self):
        path = self.get_contract_path('ContractInterfaceTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_contract_interface_decorator_too_many_arguments(self):
        path = self.get_contract_path('ContractInterfaceTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_contract_interface_decorator_without_call(self):
        path = self.get_contract_path('ContractInterfaceWithoutCall.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_contract_interface_with_instance_method(self):
        path = self.get_contract_path('ContractInterfaceInstanceMethod.py')
        self.assertCompilerLogs(CompilerError.InvalidUsage, path)

    def test_contract_interface_with_class_method(self):
        path = self.get_contract_path('ContractInterfaceClassMethod.py')
        self.assertCompilerLogs(CompilerError.InvalidUsage, path)

    def test_contract_interface_nep17(self):
        path, _ = self.get_deploy_file_paths('Nep17Interface.py')
        nep17_path, _ = self.get_deploy_file_paths('examples', 'nep17.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        nep17_call = runner.call_contract(nep17_path, 'symbol')
        invokes.append(runner.call_contract(path, 'nep17_symbol'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        nep17_result = nep17_call.result
        expected_results.append(nep17_result)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_contract_interface_display_name_argument(self):
        path = self.get_contract_path('ContractInterfaceDisplayNameRegularArgument.py')
        self.compile(path)  # test if compiles because the smart contract doesn't exist

    def test_contract_interface_display_name_keyword_argument(self):
        path = self.get_contract_path('ContractInterfaceDisplayNameKeywordArgument.py')
        self.compile(path)  # test if compiles because the smart contract doesn't exist

    def test_contract_interface_display_name_variable_name(self):
        path = self.get_contract_path('ContractInterfaceDisplayNameVariableArgument.py')
        self.assertCompilerLogs(CompilerError.InvalidUsage, path)

    def test_contract_interface_display_name_too_few_arguments(self):
        path = self.get_contract_path('ContractInterfaceDisplayNameTooFewArguments.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_contract_interface_display_name_without_call(self):
        path = self.get_contract_path('ContractInterfaceDisplayNameWithoutCall.py')
        self.assertCompilerLogs(CompilerError.UnfilledArgument, path)

    def test_contract_interface_display_name_too_many_arguments(self):
        path = self.get_contract_path('ContractInterfaceDisplayNameTooManyArguments.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_contract_interface_nep17_with_display_name(self):
        path, _ = self.get_deploy_file_paths('Nep17InterfaceWithDisplayName.py')
        nep17_path, _ = self.get_deploy_file_paths('examples', 'nep17.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        nep17_call = runner.call_contract(nep17_path, 'totalSupply')
        invokes.append(runner.call_contract(path, 'nep17_total_supply'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        nep17_result = nep17_call.result
        expected_results.append(nep17_result)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_contract_interface_code_optimization(self):
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        from boa3.internal.neo.vm.type.Integer import Integer
        from boa3.internal.neo.vm.type.String import String
        from boa3.internal.neo3.core.types import UInt160

        nep17_path, _ = self.get_deploy_file_paths('examples', 'nep17.py')
        runner = BoaTestRunner(runner_id=self.method_name())
        nep17_contract = runner.deploy_contract(nep17_path)
        runner.update_contracts(export_checkpoint=True)

        external_contract_name = 'symbol'
        function_name_bytes = String(external_contract_name).to_bytes()
        contract_script_bytes = nep17_contract.script_hash
        contract_script_hex_str = str(UInt160(contract_script_bytes))

        expected_output = (
            Opcode.NEWARRAY0    # arguments list
            + Opcode.PUSH15     # CallFlag
            + Opcode.PUSHDATA1  # function name
            + Integer(len(function_name_bytes)).to_byte_array()
            + function_name_bytes
            + Opcode.PUSHDATA1  # contract script
            + Integer(len(contract_script_bytes)).to_byte_array()
            + contract_script_bytes
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('ContractInterfaceCodeOptimization.py')
        output, manifest = self.compile_and_save(path)

        self.assertEqual(expected_output, output)
        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertIn({'contract': contract_script_hex_str,
                       'methods': [external_contract_name]
                       },
                      manifest['permissions'])

        path, _ = self.get_deploy_file_paths(path)

        invokes = []
        expected_results = []

        nep17_call = runner.call_contract(nep17_path, 'symbol')
        invokes.append(runner.call_contract(path, 'nep17_symbol'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        nep17_result = nep17_call.result
        expected_results.append(nep17_result)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_contract_manual_interface_code_optimization(self):
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        from boa3.internal.neo.vm.type.Integer import Integer
        from boa3.internal.neo.vm.type.String import String

        nep17_path, _ = self.get_deploy_file_paths('examples', 'nep17.py')
        runner = BoaTestRunner(runner_id=self.method_name())
        nep17_contract = runner.deploy_contract(nep17_path)
        runner.update_contracts(export_checkpoint=True)

        external_contract_name = 'symbol'
        function_name_bytes = String(external_contract_name).to_bytes()
        contract_script_bytes = nep17_contract.script_hash

        expected_output = (
            # start public method
            Opcode.LDSFLD0      # generated cls arg
            + Opcode.CALL
            + Integer(35).to_byte_array()
            + Opcode.RET
            # end public method
            # start initialize method
            + Opcode.INITSSLOT + b'\x01'
            + Opcode.PUSH1
            + Opcode.NEWARRAY
            + Opcode.STSFLD0
            + Opcode.PUSHDATA1
            + Integer(len(contract_script_bytes)).to_byte_array()
            + contract_script_bytes
            + Opcode.PUSH0
            + Opcode.LDSFLD0
            + Opcode.REVERSE3
            + Opcode.SETITEM
            + Opcode.RET
            # end initialize method
            # start 'symbol' class method
            + Opcode.INITSLOT + b'\x00\x01'
            + Opcode.NEWARRAY0    # arguments list
            + Opcode.PUSH15     # CallFlag
            + Opcode.PUSHDATA1  # function name
            + Integer(len(function_name_bytes)).to_byte_array()
            + function_name_bytes
            + Opcode.LDARG0     # contract script
            + Opcode.PUSH0
            + Opcode.PICKITEM
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
            # start class method
        )

        path = self.get_contract_path('ContractManualInterfaceCodeOptimization.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        path, _ = self.get_deploy_file_paths(path)

        invokes = []
        expected_results = []

        nep17_call = runner.call_contract(nep17_path, 'symbol')
        invokes.append(runner.call_contract(path, 'nep17_symbol'))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        nep17_result = nep17_call.result
        expected_results.append(nep17_result)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_get_hash(self):
        path, _ = self.get_deploy_file_paths('ContractInterfaceGetHash.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        contract_script_bytes = bytes(reversed(range(20)))
        invokes.append(runner.call_contract(path, 'main',
                                            expected_result_type=bytes))
        expected_results.append(contract_script_bytes)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_get_hash_on_metadata(self):
        path = self.get_contract_path('ContractInterfaceGetHashOnMetadata.py')
        _, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertIn({'contract': '0x000102030405060708090a0b0c0d0e0f10111213',
                       'methods': '*'
                       },
                      manifest['permissions'])

        path, _ = self.get_deploy_file_paths(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        contract_script_bytes = bytes(reversed(range(20)))
        invokes.append(runner.call_contract(path, 'main',
                                            expected_result_type=bytes))
        expected_results.append(contract_script_bytes)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
