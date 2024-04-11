from neo3.core import types

from boa3.internal.exception import CompilerError
from boa3_test.tests import boatestcase


class TestContractInterface(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/contract_interface_test'
    nep17_contract: types.UInt160

    @classmethod
    async def asyncSetupClass(cls) -> None:
        await super().asyncSetupClass()
        cls.nep17_contract = await cls.compile_and_deploy('examples', 'nep17.py')

    def test_contract_interface_decorator_literal_hash_str(self):
        path = self.get_contract_path('ContractInterfaceLiteralStrHash.py')
        self.compile(path)  # test if compiles because the smart contract doesn't exist

    def test_contract_interface_decorator_literal_hash_bytes(self):
        path = self.get_contract_path('ContractInterfaceLiteralBytesHash.py')
        self.compile(path)  # test if compiles because the smart contract doesn't exist

    def test_contract_interface_decorator_invalid_hash(self):
        self.assertCompilerLogs(CompilerError.InvalidUsage, 'ContractInterfaceInvalidHash.py')

    def test_contract_interface_decorator_variable_hash(self):
        self.assertCompilerLogs(CompilerError.InvalidUsage, 'ContractInterfaceVariableArgument.py')

    def test_contract_interface_decorator_too_few_arguments(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'ContractInterfaceTooFewArguments.py')

    def test_contract_interface_decorator_too_many_arguments(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'ContractInterfaceTooManyArguments.py')

    def test_contract_interface_decorator_without_call(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'ContractInterfaceWithoutCall.py')

    def test_contract_interface_with_instance_method(self):
        self.assertCompilerLogs(CompilerError.InvalidUsage, 'ContractInterfaceInstanceMethod.py')

    def test_contract_interface_with_class_method(self):
        self.assertCompilerLogs(CompilerError.InvalidUsage, 'ContractInterfaceClassMethod.py')

    async def test_contract_interface_nep17(self):
        await self.set_up_contract('Nep17Interface.py')

        result, _ = await self.call('nep17_symbol', [], return_type=str)
        nep17_result, _ = await self.call('symbol', [], return_type=str,
                                          target_contract=self.nep17_contract
                                          )
        self.assertEqual(nep17_result, result)

    def test_contract_interface_display_name_argument(self):
        path = self.get_contract_path('ContractInterfaceDisplayNameRegularArgument.py')
        self.compile(path)  # test if compiles because the smart contract doesn't exist

    def test_contract_interface_display_name_keyword_argument(self):
        path = self.get_contract_path('ContractInterfaceDisplayNameKeywordArgument.py')
        self.compile(path)  # test if compiles because the smart contract doesn't exist

    def test_contract_interface_display_name_variable_name(self):
        self.assertCompilerLogs(CompilerError.InvalidUsage, 'ContractInterfaceDisplayNameVariableArgument.py')

    def test_contract_interface_display_name_too_few_arguments(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'ContractInterfaceDisplayNameTooFewArguments.py')

    def test_contract_interface_display_name_without_call(self):
        self.assertCompilerLogs(CompilerError.UnfilledArgument, 'ContractInterfaceDisplayNameWithoutCall.py')

    def test_contract_interface_display_name_too_many_arguments(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'ContractInterfaceDisplayNameTooManyArguments.py')

    async def test_contract_interface_nep17_with_display_name(self):
        await self.set_up_contract('Nep17InterfaceWithDisplayName.py')

        result, _ = await self.call('nep17_total_supply', [], return_type=int)
        nep17_result, _ = await self.call('totalSupply', [], return_type=int,
                                          target_contract=self.nep17_contract
                                          )
        self.assertEqual(nep17_result, result)

    def test_contract_interface_code_optimization_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        from boa3.internal.neo.vm.type.Integer import Integer
        from boa3.internal.neo.vm.type.String import String

        external_contract_name = 'symbol'
        function_name_bytes = String(external_contract_name).to_bytes()
        contract_script_bytes = self.nep17_contract.to_array()
        contract_script_hex_str = f'0x{self.nep17_contract}'

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

        output, manifest = self.assertCompile('ContractInterfaceCodeOptimization.py',
                                              get_manifest=True
                                              )

        self.assertEqual(expected_output, output)
        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertIn({'contract': contract_script_hex_str,
                       'methods': [external_contract_name]
                       },
                      manifest['permissions'])

    async def test_contract_interface_code_optimization_run(self):
        await self.set_up_contract('ContractInterfaceCodeOptimization.py')

        result, _ = await self.call('nep17_symbol', [], return_type=str)
        nep17_result, _ = await self.call('symbol', [], return_type=str,
                                          target_contract=self.nep17_contract
                                          )
        self.assertEqual(nep17_result, result)

    def test_contract_manual_interface_code_optimization_compile(self):
        from boa3.internal.model.builtin.interop.interop import Interop
        from boa3.internal.neo.vm.opcode.Opcode import Opcode
        from boa3.internal.neo.vm.type.Integer import Integer
        from boa3.internal.neo.vm.type.String import String

        external_contract_name = 'symbol'
        function_name_bytes = String(external_contract_name).to_bytes()
        contract_script_bytes = self.nep17_contract.to_array()

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

        output, _ = self.assertCompile('ContractManualInterfaceCodeOptimization.py')
        self.assertEqual(expected_output, output)

    async def test_contract_manual_interface_code_optimization_run(self):
        await self.set_up_contract('ContractManualInterfaceCodeOptimization.py')

        result, _ = await self.call('nep17_symbol', [], return_type=str)
        nep17_result, _ = await self.call('symbol', [], return_type=str,
                                          target_contract=self.nep17_contract
                                          )
        self.assertEqual(nep17_result, result)

    async def test_get_hash(self):
        await self.set_up_contract('ContractInterfaceGetHash.py')

        contract_script = types.UInt160.from_string('0x000102030405060708090A0B0C0D0E0F10111213')
        result, _ = await self.call('main', [], return_type=types.UInt160)
        self.assertEqual(contract_script, result)

    def test_get_hash_on_metadata_compile(self):
        _, manifest = self.assertCompile('ContractInterfaceGetHashOnMetadata.py',
                                         get_manifest=True
                                         )

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertIn({'contract': '0x000102030405060708090a0b0c0d0e0f10111213',
                       'methods': '*'
                       },
                      manifest['permissions'])

    async def test_get_hash_on_metadata_run(self):
        await self.set_up_contract('ContractInterfaceGetHashOnMetadata.py')

        contract_script = types.UInt160.from_string('0x000102030405060708090A0B0C0D0E0F10111213')
        result, _ = await self.call('main', [], return_type=types.UInt160)
        self.assertEqual(contract_script, result)
