from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal import constants
from boa3.internal.constants import IMPORT_WILDCARD
from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo3.core.types import UInt160
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_classes.contract.neomanifeststruct import NeoManifestStruct
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestMetadata(BoaTest):
    default_folder: str = 'test_sc/metadata_test'

    def test_metadata_info_method(self):
        expected_output = (
            Opcode.PUSH5  # return 5
            + Opcode.RET
        )

        path = self.get_contract_path('MetadataInfoMethod.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        # test extra field
        self.assertIn('extra', manifest)
        self.assertIsNone(manifest['extra'])

    def test_metadata_info_method_with_decorator(self):
        expected_output = (
            Opcode.PUSH5  # return 5
            + Opcode.RET
        )

        path = self.get_contract_path('MetadataInfoWithDecorator.py')
        output = self.assertCompilerLogs(CompilerWarning.DeprecatedSymbol, path)
        self.assertEqual(expected_output, output)

    def test_metadata_info_method_mismatched_type(self):
        path = self.get_contract_path('MetadataInfoMethodMismatchedReturn.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_metadata_info_method_no_return(self):
        path = self.get_contract_path('MetadataInfoMethodNoReturn.py')
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, path)

    def test_metadata_info_multiple_method(self):
        expected_output = (
            Opcode.PUSH5  # return 5
            + Opcode.RET
        )

        path = self.get_contract_path('MetadataInfoMultipleMethod.py')
        self.assertCompilerLogs(CompilerWarning.RedeclaredSymbol, path)

        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('Description', manifest['extra'])
        self.assertEqual('func1', manifest['extra']['Description'])

    def test_metadata_method_with_args(self):
        path = self.get_contract_path('MetadataMethodWithArgs.py')
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, path)

    def test_metadata_method_called_by_user_method(self):
        path = self.get_contract_path('MetadataMethodCalledByUserMethod.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_metadata_object_call_user_method(self):
        path = self.get_contract_path('MetadataObjectCallUserMethod.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_metadata_object_type_user_method(self):
        path = self.get_contract_path('MetadataObjectTypeUserMethod.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_metadata_info_author(self):
        expected_output = (
            Opcode.PUSH5  # return 5
            + Opcode.RET
        )

        path = self.get_contract_path('MetadataInfoAuthor.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('Author', manifest['extra'])
        self.assertEqual('Test', manifest['extra']['Author'])

    def test_metadata_info_author_mismatched_type(self):
        path = self.get_contract_path('MetadataInfoAuthorMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_metadata_info_email(self):
        expected_output = (
            Opcode.PUSH5  # return 5
            + Opcode.RET
        )

        path = self.get_contract_path('MetadataInfoEmail.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('Email', manifest['extra'])
        self.assertEqual('test@test.com', manifest['extra']['Email'])

    def test_metadata_info_email_mismatched_type(self):
        path = self.get_contract_path('MetadataInfoEmailMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_metadata_info_description(self):
        expected_output = (
            Opcode.PUSH5  # return 5
            + Opcode.RET
        )

        path = self.get_contract_path('MetadataInfoDescription.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('Description', manifest['extra'])
        self.assertEqual('This is an example', manifest['extra']['Description'])

    def test_metadata_info_description_mismatched_type(self):
        path = self.get_contract_path('MetadataInfoDescriptionMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_metadata_info_extras(self):
        expected_output = (
            Opcode.PUSH5  # return 5
            + Opcode.RET
        )

        path = self.get_contract_path('MetadataInfoExtras.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('Author', manifest['extra'])
        self.assertEqual('Test', manifest['extra']['Author'])
        self.assertIn('Email', manifest['extra'])
        self.assertEqual('test@test.com', manifest['extra']['Email'])
        self.assertIn('Description', manifest['extra'])
        self.assertEqual('This is an example', manifest['extra']['Description'])

    def test_metadata_info_new_extras(self):
        expected_output = (
            Opcode.PUSH5  # return 5
            + Opcode.RET
        )

        path = self.get_contract_path('MetadataInfoNewExtras.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)
        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('UnitTest1', manifest['extra'])
        self.assertEqual('string', manifest['extra']['UnitTest1'])
        self.assertIn('UnitTest2', manifest['extra'])
        self.assertEqual(123, manifest['extra']['UnitTest2'])
        self.assertIn('UnitTest3', manifest['extra'])
        self.assertEqual(True, manifest['extra']['UnitTest3'])
        self.assertIn('UnitTest4', manifest['extra'])
        self.assertEqual(['list', 3210], manifest['extra']['UnitTest4'])

    def test_metadata_info_supported_standards(self):
        path = self.get_contract_path('MetadataInfoSupportedStandards.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-17', manifest['supportedstandards'])

        nef, manifest = self.get_bytes_output(path)
        path, _ = self.get_deploy_file_paths(path)
        get_contract_path, _ = self.get_deploy_file_paths('test_sc/native_test/contractmanagement', 'GetContract.py')

        runner = BoaTestRunner(runner_id=self.method_name())
        # verify using NeoManifestStruct
        contract = runner.deploy_contract(path)
        runner.update_contracts(export_checkpoint=True)
        call_hash = contract.script_hash

        invoke = runner.call_contract(get_contract_path, 'main', call_hash)
        manifest_struct = NeoManifestStruct.from_json(manifest)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(manifest_struct, invoke.result[4])

    def test_metadata_info_supported_standards_from_package(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsEventFromPackage.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-17', manifest['supportedstandards'])

        nef, manifest = self.get_bytes_output(path)
        path, _ = self.get_deploy_file_paths(path)
        get_contract_path, _ = self.get_deploy_file_paths('test_sc/native_test/contractmanagement', 'GetContract.py')

        runner = BoaTestRunner(runner_id=self.method_name())
        # verify using NeoManifestStruct
        contract = runner.deploy_contract(path)
        runner.update_contracts(export_checkpoint=True)
        call_hash = contract.script_hash

        invoke = runner.call_contract(get_contract_path, 'main', call_hash)
        manifest_struct = NeoManifestStruct.from_json(manifest)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(manifest_struct, invoke.result[4])

    def test_metadata_info_supported_standards_with_imported_event(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsImportedEvent.py')
        output, manifest = self.get_output(path)

        self.assertIn('abi', manifest)
        abi = manifest['abi']

        self.assertIn('events', abi)
        self.assertEqual(1, len(abi['events']))

        self.assertIn('name', abi['events'][0])
        self.assertEqual('Transfer', abi['events'][0]['name'])

    def test_metadata_info_supported_standards_filter(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsFilter.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-17', manifest['supportedstandards'])

        # Using a dot is permitted and won't be removed by the filter
        self.assertIn('NEP-17.1', manifest['supportedstandards'])
        self.assertIn('NEP-17.1.2', manifest['supportedstandards'])
        self.assertIn('NEP-17.1.3.5.7.9.11.13', manifest['supportedstandards'])     # possible to use more than 1 dot

        # Every NEP needs to be in uppercase and be separated by a dash
        self.assertIn('NEP-100', manifest['supportedstandards'])
        self.assertIn('NEP-101', manifest['supportedstandards'])
        self.assertIn('NEP-102', manifest['supportedstandards'])

        # Standards that doesn't begin with NEP will not the filtered
        self.assertIn('not neo standard 1', manifest['supportedstandards'])

    def test_metadata_info_supported_standards_not_explicit(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsNotExplicit.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-17', manifest['supportedstandards'])

    def test_metadata_info_supported_standards_not_explicit_incomplete_methods(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsNotExplicitIncompleteMethods.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertEqual(len(manifest['supportedstandards']), 0)

    def test_metadata_info_supported_standards_not_explicit_incomplete_events(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsNotExplicitIncompleteEvents.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertEqual(len(manifest['supportedstandards']), 0)

    def test_metadata_info_supported_standards_missing_implementations_nep17(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsMissingImplementationNEP17.py')
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, path)

    def test_metadata_info_supported_standards_nep11_divisible(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsNEP11Divisible.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-11', manifest['supportedstandards'])

    def test_metadata_info_supported_standards_nep11_divisible_optional_methods(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsNEP11DivisibleOptionalMethods.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-11', manifest['supportedstandards'])

    def test_metadata_info_supported_standards_nep11_non_divisible(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsNEP11NonDivisible.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-11', manifest['supportedstandards'])

    def test_metadata_info_supported_standards_nep11_non_divisible_optional_methods(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsNEP11NonDivisibleOptionalMethods.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-11', manifest['supportedstandards'])

    def test_metadata_info_supported_standards_missing_implementations_nep11(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsMissingImplementationNEP11.py')
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, path)

    def test_metadata_info_supported_standards_missing_implementations_nep11_divisible(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsMissingImplementationNEP11Divisible.py')
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, path)

    def test_metadata_info_supported_standards_missing_implementations_nep11_optional_method(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsMissingImplementationNEP11OptionalMethods.py')
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, path)

    def test_metadata_info_supported_standards_missing_event_nep11(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsMissingEventNEP11.py')
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, path)

    def test_metadata_info_supported_standards_mismatched_type(self):
        path = self.get_contract_path('MetadataInfoDescriptionMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_metadata_info_supported_standards_bytestring_as_bytes(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsByteStringAsBytes.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-11', manifest['supportedstandards'])

    def test_metadata_info_supported_standards_bytestring_as_str(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsByteStringAsStr.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-11', manifest['supportedstandards'])

    def test_metadata_info_trusts(self):
        path = self.get_contract_path('MetadataInfoTrusts.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('trusts', manifest)
        self.assertIsInstance(manifest['trusts'], list)
        self.assertEqual(len(manifest['trusts']), 4)
        self.assertIn('0x1234567890123456789012345678901234567890', manifest['trusts'])
        self.assertIn('0x1234567890123456789012345678901234abcdef', manifest['trusts'])
        self.assertIn('035a928f201639204e06b4368b1a93365462a8ebbff0b8818151b74faab3a2b61a', manifest['trusts'])
        self.assertIn('03cdb067d930fd5adaa6c68545016044aaddec64ba39e548250eaea551172e535c', manifest['trusts'])

        nef, manifest = self.get_bytes_output(path)
        path, _ = self.get_deploy_file_paths(path)
        get_contract_path, _ = self.get_deploy_file_paths('test_sc/native_test/contractmanagement', 'GetContract.py')

        runner = BoaTestRunner(runner_id=self.method_name())
        # verify using NeoManifestStruct
        contract = runner.deploy_contract(path)
        runner.update_contracts(export_checkpoint=True)
        call_hash = contract.script_hash

        invoke = runner.call_contract(get_contract_path, 'main', call_hash)
        manifest_struct = NeoManifestStruct.from_json(manifest)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        result_trusts = invoke.result[4][6]

        # transform the str values to bytes values
        manifest_struct_trusts = []
        for item in manifest_struct[6]:
            if isinstance(item, str):
                if len(item) == 42:
                    from boa3.internal.neo3.core.types import UInt160
                    item = UInt160.from_string(item).to_array()
                elif len(item) == 66:
                    item = bytes.fromhex(item)
            manifest_struct_trusts.append(item)

        # compare result from GetContract and NeoManifestStruct
        self.assertEqual(manifest_struct_trusts, result_trusts)

    def test_metadata_info_trusts_wildcard(self):
        path = self.get_contract_path('MetadataInfoTrustsWildcard.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('trusts', manifest)
        self.assertIsInstance(manifest['trusts'], str)
        self.assertEqual(IMPORT_WILDCARD, manifest['trusts'])

        path, _ = self.get_deploy_file_paths(path)
        get_contract_path, _ = self.get_deploy_file_paths('test_sc/native_test/contractmanagement', 'GetContract.py')

        runner = BoaTestRunner(runner_id=self.method_name())
        # verify using NeoManifestStruct
        contract = runner.deploy_contract(path)
        runner.update_contracts(export_checkpoint=True)
        call_hash = contract.script_hash

        invoke = runner.call_contract(get_contract_path, 'main', call_hash)
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        result_trusts = invoke.result[4][6]
        self.assertEqual(None, result_trusts)

    def test_metadata_info_trusts_mismatched_types(self):
        path = self.get_contract_path('MetadataInfoTrustsMismatchedTypes.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('trusts', manifest)
        self.assertIsInstance(manifest['trusts'], list)
        self.assertEqual(len(manifest['trusts']), 0)

    def test_metadata_info_trusts_default(self):
        path = self.get_contract_path('MetadataInfoDefault.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('trusts', manifest)
        self.assertIsInstance(manifest['trusts'], list)
        self.assertEqual(len(manifest['trusts']), 0)

    def test_metadata_info_permissions(self):
        path = self.get_contract_path('MetadataInfoPermissions.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 3)
        self.assertIn({"contract": "*", "methods": ['onNEP17Payment']}, manifest['permissions'])
        self.assertIn({"contract": "0x3846a4aa420d9831044396dd3a56011514cd10e3", "methods": ["get_object"]}, manifest['permissions'])
        self.assertIn({"contract": "0333b24ee50a488caa5deec7e021ff515f57b7993b93b45d7df901e23ee3004916", "methods": "*"}, manifest['permissions'])

        nef, manifest = self.get_bytes_output(path)
        path, _ = self.get_deploy_file_paths(path)
        get_contract_path, _ = self.get_deploy_file_paths('test_sc/native_test/contractmanagement', 'GetContract.py')

        runner = BoaTestRunner(runner_id=self.method_name())
        # verify using NeoManifestStruct
        contract = runner.deploy_contract(path)
        runner.update_contracts(export_checkpoint=True)
        call_hash = contract.script_hash

        invoke = runner.call_contract(get_contract_path, 'main', call_hash)
        manifest_struct = NeoManifestStruct.from_json(manifest)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        result_permissions = invoke.result[4][5]

        # casting the addresses to bytes values
        manifest_struct_permissions = []
        for item in manifest_struct[5]:
            contract = item[0]

            from boa3.internal.neo3.core.types import UInt160
            if isinstance(contract, UInt160):
                contract = contract.to_array()
            manifest_struct_permissions.append([contract, item[1]])

        # compare result from GetContract and NeoManifestStruct
        self.assertEqual(manifest_struct_permissions, result_permissions)

    def test_metadata_info_permissions_mismatched_type(self):
        path = self.get_contract_path('MetadataInfoPermissionsMismatchedType.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 0)

    def test_metadata_info_permissions_default(self):
        path = self.get_contract_path('MetadataInfoDefault.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 0)

    def test_metadata_info_permissions_wildcard(self):
        path = self.get_contract_path('MetadataInfoPermissionsWildcard.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn({"contract": "*", "methods": "*"}, manifest['permissions'])

        path, _ = self.get_deploy_file_paths_without_compiling(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'main')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)
        self.assertEqual(invoke.result, 100_000_000)    # NEO total supply

    def test_metadata_info_permissions_native_contract(self):
        path = self.get_contract_path('MetadataInfoPermissionsNativeContract.py')
        output, manifest = self.compile_and_save(path)

        expected_permission = {
            'contract': str(UInt160(constants.MANAGEMENT_SCRIPT)),
            'methods': ['update', 'destroy']
        }
        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn(expected_permission, manifest['permissions'])

    def test_metadata_info_permissions_invalid_call(self):
        path = self.get_contract_path('MetadataInfoPermissionsInvalidCall.py')
        output, manifest = self.compile_and_save(path)

        expected_permission = {
            'contract': '0x0102030405060708090A0B0C0D0E0F1011121314'.lower(),
            'methods': '*'
        }
        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn(expected_permission, manifest['permissions'])

        path, _ = self.get_deploy_file_paths_without_compiling(path)
        runner = BoaTestRunner(runner_id=self.method_name())

        runner.call_contract(path, 'main')

        runner.execute()
        self.assertEqual(VMState.FAULT, runner.vm_state, msg=runner.cli_log)
        self.assertRegex(runner.error, f'^{self.CANT_CALL_METHOD_PREFIX}')

    def test_metadata_info_name(self):
        path = self.get_contract_path('MetadataInfoName.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('name', manifest)
        self.assertIsInstance(manifest['name'], str)
        self.assertGreater(len(manifest['name']), 0)
        self.assertEqual((manifest['name']), "SmartContractCustomName")

    def test_metadata_info_name_default(self):
        path = self.get_contract_path('MetadataInfoDefault.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('name', manifest)
        self.assertIsInstance(manifest['name'], str)
        self.assertGreater(len(manifest['name']), 0)
        self.assertEqual((manifest['name']), "MetadataInfoDefault")

    def test_metadata_info_name_mismatched_type(self):
        path = self.get_contract_path('MetadataInfoNameMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_metadata_info_groups(self):
        path = self.get_contract_path('MetadataInfoGroups.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('groups', manifest)
        self.assertIsInstance(manifest['groups'], list)
        self.assertEqual(len(manifest['groups']), 1)
        self.assertIn({'pubkey': '031f64da8a38e6c1e5423a72ddd6d4fc4a777abe537e5cb5aa0425685cda8e063b',
                       'signature': 'fhsOJNF3N5Pm3oV1b7wYTx0QVelYNu7whwXMi8GsNGFKUnu3ZG8z7oWLfzzEz9pbnzwQe8WFCALEiZhLD1jG/w=='}, manifest['groups'])

        nef, manifest = self.get_bytes_output(path)
        path, _ = self.get_deploy_file_paths(path)
        get_contract_path, _ = self.get_deploy_file_paths('test_sc/native_test/contractmanagement', 'GetContract.py')

        runner = BoaTestRunner(runner_id=self.method_name())
        # verify using NeoManifestStruct
        contract_call = runner.call_contract(path, 'main')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        call_hash = contract_call.invoke.contract.script_hash
        invoke = runner.call_contract(get_contract_path, 'main', call_hash)
        manifest_struct = NeoManifestStruct.from_json(manifest)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        result_groups = []
        for group in invoke.result[4][1]:
            dict_group = {'pubkey': group[0].hex()}
            import base64
            # getContract returns the signature without the base64 encoding
            dict_group['signature'] = base64.b64encode(group[1]).decode('utf-8')
            result_groups.append(dict_group)

        manifest_struct_groups = manifest_struct[1]

        self.assertEqual(manifest_struct_groups, result_groups)

    def test_metadata_info_groups_default(self):
        path = self.get_contract_path('MetadataInfoDefault.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('groups', manifest)
        self.assertIsInstance(manifest['groups'], list)
        self.assertEqual(len(manifest['groups']), 0)

    def test_metadata_info_source(self):
        path = self.get_contract_path('MetadataInfoSource.py')
        self.compile_and_save(path)

        nef_path, _ = self.get_deploy_file_paths_without_compiling(path)
        with open(nef_path, mode='rb') as nef:
            from boa3.internal.neo.contracts.neffile import NefFile
            generated_source = NefFile.deserialize(nef.read()).source

        self.assertEqual(generated_source, 'https://github.com/CityOfZion/neo3-boa')

    def test_metadata_info_source_default(self):
        path = self.get_contract_path('MetadataInfoDefault.py')
        self.compile_and_save(path)

        nef_path, _ = self.get_deploy_file_paths_without_compiling(path)
        with open(nef_path, mode='rb') as nef:
            from boa3.internal.neo.contracts.neffile import NefFile
            generated_source = NefFile.deserialize(nef.read()).source

        self.assertEqual(generated_source, '')

    def test_metadata_info_source_mismatched_type(self):
        path = self.get_contract_path('MetadataInfoSourceMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_metadata_importing_external_contract_before_metadata_method(self):
        path = self.get_contract_path('MetadataImportingExternalContractBeforeMetadataMethod.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('extra', manifest)
        self.assertIsInstance(manifest['extra'], dict)
        self.assertIn('Description', manifest['extra'])
        self.assertEqual(manifest['extra']['Description'], 'Test importing a external contract before declaring the metadata')

        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertEqual(manifest['permissions'][0]['contract'], '0x1234567890123456789012345678901234567890')
