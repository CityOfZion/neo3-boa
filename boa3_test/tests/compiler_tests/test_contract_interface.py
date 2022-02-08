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

        self.compile_and_save(path)
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

        self.compile_and_save(path)
        engine = TestEngine()

        nep17_result = self.run_smart_contract(engine, nep17_path, 'totalSupply')
        result = self.run_smart_contract(engine, path, 'nep17_total_supply')
        self.assertEqual(nep17_result, result)
