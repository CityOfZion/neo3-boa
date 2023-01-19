from boa3.boa3 import Boa3
from boa3.exception import CompilerError
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestContractInterface(BoaTest):
    default_folder: str = 'test_sc/contract_interface_test'

    def test_contract_interface_decorator_literal_hash_str(self):
        path = self.get_contract_path('ContractInterfaceLiteralStrHash.py')
        Boa3.compile(path)  # test if compiles because the smart contract doesn't exist

    def test_contract_interface_decorator_literal_hash_bytes(self):
        path = self.get_contract_path('ContractInterfaceLiteralBytesHash.py')
        Boa3.compile(path)  # test if compiles because the smart contract doesn't exist

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
        path = self.get_contract_path('Nep17Interface.py')
        nep17_path = self.get_contract_path('examples', 'nep17.py')

        engine = TestEngine()

        nep17_result = self.run_smart_contract(engine, nep17_path, 'symbol')
        result = self.run_smart_contract(engine, path, 'nep17_symbol')
        self.assertEqual(nep17_result, result)

    def test_contract_interface_display_name_argument(self):
        path = self.get_contract_path('ContractInterfaceDisplayNameRegularArgument.py')
        Boa3.compile(path)  # test if compiles because the smart contract doesn't exist

    def test_contract_interface_display_name_keyword_argument(self):
        path = self.get_contract_path('ContractInterfaceDisplayNameKeywordArgument.py')
        Boa3.compile(path)  # test if compiles because the smart contract doesn't exist

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
        path = self.get_contract_path('Nep17InterfaceWithDisplayName.py')
        nep17_path = self.get_contract_path('examples', 'nep17.py')

        engine = TestEngine()

        nep17_result = self.run_smart_contract(engine, nep17_path, 'totalSupply')
        result = self.run_smart_contract(engine, path, 'nep17_total_supply')
        self.assertEqual(nep17_result, result)

    def test_contract_interface_code_optimization(self):
        from boa3.model.builtin.interop.interop import Interop
        from boa3.neo.vm.opcode.Opcode import Opcode
        from boa3.neo.vm.type.Integer import Integer
        from boa3.neo.vm.type.String import String
        from boa3.neo3.core.types import UInt160

        external_contract_name = 'symbol'
        function_name_bytes = String(external_contract_name).to_bytes()
        contract_script_bytes = UInt160.from_string('cc370e7538a8729221e6eb444eb6f8838d256042').to_array()

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

        nep17_path = self.get_contract_path('examples', 'nep17.py')
        engine = TestEngine()

        nep17_result = self.run_smart_contract(engine, nep17_path, 'symbol')
        result = self.run_smart_contract(engine, path, 'nep17_symbol')
        self.assertEqual(nep17_result, result)

    def test_contract_manual_interface_code_optimization(self):
        from boa3.model.builtin.interop.interop import Interop
        from boa3.neo.vm.opcode.Opcode import Opcode
        from boa3.neo.vm.type.Integer import Integer
        from boa3.neo.vm.type.String import String
        from boa3.neo3.core.types import UInt160

        external_contract_name = 'symbol'
        function_name_bytes = String(external_contract_name).to_bytes()
        contract_script_bytes = UInt160.from_string('cc370e7538a8729221e6eb444eb6f8838d256042').to_array()

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

        nep17_path = self.get_contract_path('examples', 'nep17.py')
        engine = TestEngine()

        nep17_result = self.run_smart_contract(engine, nep17_path, 'symbol')
        result = self.run_smart_contract(engine, path, 'nep17_symbol')
        self.assertEqual(nep17_result, result)

    def test_get_hash(self):
        path = self.get_contract_path('ContractInterfaceGetHash.py')
        engine = TestEngine()

        contract_script_bytes = bytes(reversed(range(20)))
        result = self.run_smart_contract(engine, path, 'main',
                                         expected_result_type=bytes)
        self.assertEqual(contract_script_bytes, result)
