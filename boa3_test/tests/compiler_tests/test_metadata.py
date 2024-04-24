from neo3.core import types

from boa3.internal import constants
from boa3.internal.constants import IMPORT_WILDCARD
from boa3.internal.exception import CompilerError, CompilerWarning
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests import boatestcase
from boa3_test.tests.test_classes.contract.neomanifeststruct import NeoManifestStruct


class TestMetadata(boatestcase.BoaTestCase):
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

    def test_metadata_info_method_no_return(self):
        self.assertCompilerLogs(CompilerError.MissingReturnStatement, 'MetadataInfoMethodNoReturn.py')

    def test_metadata_info_multiple_method(self):
        expected_output = (
            Opcode.PUSH5  # return 5
            + Opcode.RET
        )

        output, manifest = self.assertCompilerLogs(CompilerWarning.RedeclaredSymbol, 'MetadataInfoMultipleMethod.py')

        self.assertEqual(expected_output, output)

        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('Description', manifest['extra'])
        self.assertEqual('func1', manifest['extra']['Description'])

    def test_metadata_method_with_args(self):
        self.assertCompilerLogs(CompilerError.UnexpectedArgument, 'MetadataMethodWithArgs.py')

    def test_metadata_method_called_by_user_method(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'MetadataMethodCalledByUserMethod.py')

    def test_metadata_object_call_user_method(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'MetadataObjectCallUserMethod.py')

    def test_metadata_object_type_user_method(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'MetadataObjectTypeUserMethod.py')

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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MetadataInfoAuthorMismatchedType.py')

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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MetadataInfoEmailMismatchedType.py')

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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MetadataInfoDescriptionMismatchedType.py')

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

    async def test_metadata_info_supported_standards(self):
        path = self.get_contract_path('MetadataInfoSupportedStandards.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-17', manifest['supportedstandards'])

        await self.set_up_contract('test_sc/native_test/contractmanagement', 'GetContract.py')
        contract = await self.compile_and_deploy(path)

        call_hash = contract.to_array()
        result, _ = await self.call('main', [call_hash], return_type=list)
        self.assertGreater(len(result), 4)

        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

    async def test_metadata_info_supported_standards_from_package(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsEventFromPackage.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('supportedstandards', manifest)
        self.assertIsInstance(manifest['supportedstandards'], list)
        self.assertGreater(len(manifest['supportedstandards']), 0)
        self.assertIn('NEP-17', manifest['supportedstandards'])

        await self.set_up_contract('test_sc/native_test/contractmanagement', 'GetContract.py')
        contract = await self.compile_and_deploy(path)

        call_hash = contract.to_array()
        result, _ = await self.call('main', [call_hash], return_type=list)
        self.assertGreater(len(result), 4)

        manifest_struct = NeoManifestStruct.from_json(manifest)
        self.assertEqual(manifest_struct, result[4])

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
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, 'MetadataInfoSupportedStandardsMissingImplementationNEP17.py')

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
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, 'MetadataInfoSupportedStandardsMissingImplementationNEP11.py')

    def test_metadata_info_supported_standards_missing_implementations_nep11_divisible(self):
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, 'MetadataInfoSupportedStandardsMissingImplementationNEP11Divisible.py')

    def test_metadata_info_supported_standards_missing_implementations_nep11_optional_method(self):
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, 'MetadataInfoSupportedStandardsMissingImplementationNEP11OptionalMethods.py')

    def test_metadata_info_supported_standards_missing_event_nep11(self):
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, 'MetadataInfoSupportedStandardsMissingEventNEP11.py')

    def test_metadata_info_supported_standards_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MetadataInfoDescriptionMismatchedType.py')

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

    async def test_metadata_info_trusts(self):
        path = self.get_contract_path('MetadataInfoTrusts.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('trusts', manifest)
        self.assertIsInstance(manifest['trusts'], list)
        self.assertEqual(len(manifest['trusts']), 4)
        self.assertIn('0x1234567890123456789012345678901234567890', manifest['trusts'])
        self.assertIn('0x1234567890123456789012345678901234abcdef', manifest['trusts'])
        self.assertIn('035a928f201639204e06b4368b1a93365462a8ebbff0b8818151b74faab3a2b61a', manifest['trusts'])
        self.assertIn('03cdb067d930fd5adaa6c68545016044aaddec64ba39e548250eaea551172e535c', manifest['trusts'])

        await self.set_up_contract('test_sc/native_test/contractmanagement', 'GetContract.py')
        contract = await self.compile_and_deploy(path)

        call_hash = contract.to_array()
        result, _ = await self.call('main', [call_hash], return_type=list)
        self.assertGreater(len(result), 4)

        manifest_struct = NeoManifestStruct.from_json(manifest)
        result_trusts = result[4][6]

        # transform the str values to bytes values
        manifest_struct_trusts = []
        for item in manifest_struct[6]:
            if isinstance(item, str):
                if len(item) == 42:
                    item = types.UInt160.from_string(item).to_array()
                elif len(item) == 66:
                    item = bytes.fromhex(item)
            manifest_struct_trusts.append(item)

        # compare result from GetContract and NeoManifestStruct
        self.assertEqual(manifest_struct_trusts, result_trusts)

    async def test_metadata_info_trusts_wildcard(self):
        path = self.get_contract_path('MetadataInfoTrustsWildcard.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('trusts', manifest)
        self.assertIsInstance(manifest['trusts'], str)
        self.assertEqual(IMPORT_WILDCARD, manifest['trusts'])

        await self.set_up_contract('test_sc/native_test/contractmanagement', 'GetContract.py')
        contract = await self.compile_and_deploy(path)

        call_hash = contract.to_array()
        result, _ = await self.call('main', [call_hash], return_type=list)
        self.assertGreater(len(result), 4)

        result_trusts = result[4][6]
        self.assertIsNone(result_trusts)

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

    async def test_metadata_info_permissions(self):
        path = self.get_contract_path('MetadataInfoPermissions.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 3)
        self.assertIn({"contract": "*", "methods": ['onNEP17Payment']}, manifest['permissions'])
        self.assertIn({"contract": "0x3846a4aa420d9831044396dd3a56011514cd10e3", "methods": ["get_object"]}, manifest['permissions'])
        self.assertIn({"contract": "0333b24ee50a488caa5deec7e021ff515f57b7993b93b45d7df901e23ee3004916", "methods": "*"}, manifest['permissions'])

        nef, manifest = self.get_output(path)

        await self.set_up_contract('test_sc/native_test/contractmanagement', 'GetContract.py')
        contract = await self.compile_and_deploy(path)

        call_hash = contract.to_array()
        result, _ = await self.call('main', [call_hash], return_type=list)
        self.assertGreater(len(result), 4)

        manifest_struct = NeoManifestStruct.from_json(manifest)
        result_permissions = result[4][5]

        # casting the addresses to bytes values
        manifest_struct_permissions = []
        for item in manifest_struct[5]:
            contract = item[0]

            if hasattr(contract, 'to_array'):
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

    def test_metadata_info_permissions_empty_list(self):
        path = self.get_contract_path('MetadataInfoPermissionsEmptyList.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 0)

    def test_metadata_info_permissions_tuple(self):
        path = self.get_contract_path('MetadataInfoPermissionsTuple.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn({"contract": "*", "methods": ['total_supply', 'onNEP17Payment']}, manifest['permissions'])

    async def test_metadata_info_permissions_wildcard(self):
        path = self.get_contract_path('MetadataInfoPermissionsWildcard.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn({"contract": "*", "methods": "*"}, manifest['permissions'])

        await self.set_up_contract(path)

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(result, 100_000_000)    # NEO total supply

    async def test_metadata_info_permissions_wildcard_list_single_element(self):
        path = self.get_contract_path('MetadataInfoPermissionsWildcardListSingleElement.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn({"contract": "*", "methods": "*"}, manifest['permissions'])

    async def test_metadata_info_permissions_wildcard_list(self):
        path = self.get_contract_path('MetadataInfoPermissionsWildcardList.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn({"contract": "*", "methods": "*"}, manifest['permissions'])

    async def test_metadata_info_permissions_wildcard_tuple(self):
        path = self.get_contract_path('MetadataInfoPermissionsWildcardTuple.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn({"contract": "*", "methods": "*"}, manifest['permissions'])

    def test_metadata_info_permissions_native_contract(self):
        path = self.get_contract_path('MetadataInfoPermissionsNativeContract.py')
        output, manifest = self.compile_and_save(path)

        expected_permission = {
            'contract': f'0x{types.UInt160(constants.MANAGEMENT_SCRIPT)}',
            'methods': ['update', 'destroy']
        }
        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn(expected_permission, manifest['permissions'])

    async def test_metadata_info_permissions_invalid_call(self):
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

        await self.set_up_contract(path)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [], return_type=bool)

        self.assertRegex(str(context.exception), 'disallowed method call')

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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MetadataInfoNameMismatchedType.py')

    async def test_metadata_info_groups(self):
        path = self.get_contract_path('MetadataInfoGroups.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('groups', manifest)
        self.assertIsInstance(manifest['groups'], list)
        self.assertEqual(len(manifest['groups']), 1)
        self.assertIn({'pubkey': '033d523f36a732974c0f7dbdfafb5206ecd087211366a274190f05b86d357f4bad',
                       'signature': 'QqtxfL5kHskQXtH5Jmg8+OoM6ltJF5gCpZlujpE9AvdZhzfns4I2jSZaxm+evA/nLRJpQlKmupXfuj2P8viQQg=='}, manifest['groups'])

        nef, manifest = self.get_output(path)

        await self.set_up_contract('test_sc/native_test/contractmanagement', 'GetContract.py')
        call_contract = await self.compile_and_deploy(path)
        call_hash = call_contract.to_array()

        result, _ = await self.call('main', [call_hash], return_type=list)
        self.assertGreater(len(result), 4)

        manifest_struct = NeoManifestStruct.from_json(manifest)
        result_groups = []

        for group in result[4][1]:
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
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'MetadataInfoSourceMismatchedType.py')

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
