from boa3 import constants
from boa3.constants import IMPORT_WILDCARD
from boa3.exception import CompilerError, CompilerWarning
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo3.core.types import UInt160
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.contract.neomanifeststruct import NeoManifestStruct
from boa3_test.tests.test_classes.testengine import TestEngine


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

        engine = TestEngine()
        # verify using NeoManifestStruct
        nef, manifest = self.get_bytes_output(path)
        self.run_smart_contract(engine, path, 'Main')
        call_hash = engine.executed_script_hash.to_array()
        path = path.replace('.py', '.nef')

        get_contract_path = self.get_contract_path('test_sc/native_test/contractmanagement', 'GetContract.py')
        engine = TestEngine()
        engine.add_contract(path)

        result = self.run_smart_contract(engine, get_contract_path, 'main', call_hash)
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
        path = self.get_contract_path('MetadataInfoSupportedStandardsMissingImplementationNEP17.py')
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, path)

    def test_metadata_info_supported_standards_missing_implementations_nep11(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsMissingImplementationNEP11.py')
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, path)

    def test_metadata_info_supported_standards_missing_implementations_nep11_optional_method(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsMissingImplementationNEP11OptionalMethods.py')
        self.assertCompilerLogs(CompilerError.MissingStandardDefinition, path)

    def test_metadata_info_supported_standards_mismatched_type(self):
        path = self.get_contract_path('MetadataInfoDescriptionMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

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

        engine = TestEngine()
        # verify using NeoManifestStruct
        nef, manifest = self.get_bytes_output(path)
        self.run_smart_contract(engine, path, 'Main')
        call_hash = engine.executed_script_hash.to_array()
        path = path.replace('.py', '.nef')

        get_contract_path = self.get_contract_path('test_sc/native_test/contractmanagement', 'GetContract.py')
        engine = TestEngine()
        engine.add_contract(path)

        result = self.run_smart_contract(engine, get_contract_path, 'main', call_hash)
        manifest_struct = NeoManifestStruct.from_json(manifest)

        result_trusts = result[4][6]

        # transform the str values to bytes values
        manifest_struct_trusts = []
        for item in manifest_struct[6]:
            if isinstance(item, str):
                if len(item) == 42:
                    from boa3.neo3.core.types import UInt160
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
        self.assertIsInstance(manifest['trusts'], list)
        self.assertEqual(len(manifest['trusts']), 1)
        self.assertIn(IMPORT_WILDCARD, manifest['trusts'])

        engine = TestEngine()
        # verify using NeoManifestStruct
        nef, manifest = self.get_bytes_output(path)
        self.run_smart_contract(engine, path, 'Main')
        call_hash = engine.executed_script_hash.to_array()
        path = path.replace('.py', '.nef')

        get_contract_path = self.get_contract_path('test_sc/native_test/contractmanagement', 'GetContract.py')
        engine = TestEngine()
        engine.add_contract(path)

        result = self.run_smart_contract(engine, get_contract_path, 'main', call_hash)
        manifest_struct = NeoManifestStruct.from_json(manifest)

        result_trusts = result[4][6]

        # TODO: change when TestEngine is updated
        self.assertEqual([''], result_trusts)

    def test_metadata_info_trusts_mismatched_types(self):
        path = self.get_contract_path('MetadataInfoTrustsMismatchedTypes.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('trusts', manifest)
        self.assertIsInstance(manifest['trusts'], list)
        self.assertEqual(len(manifest['trusts']), 0)

    def test_metadata_info_trusts_default(self):
        path = self.get_contract_path('MetadataInfoTrustsDefault.py')
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

        engine = TestEngine()
        # verify using NeoManifestStruct
        nef, manifest = self.get_bytes_output(path)
        self.run_smart_contract(engine, path, 'Main')
        call_hash = engine.executed_script_hash.to_array()
        path = path.replace('.py', '.nef')

        get_contract_path = self.get_contract_path('test_sc/native_test/contractmanagement', 'GetContract.py')
        engine = TestEngine()
        engine.add_contract(path)

        result = self.run_smart_contract(engine, get_contract_path, 'main', call_hash)
        manifest_struct = NeoManifestStruct.from_json(manifest)

        result_permissions = result[4][5]

        # casting the addresses to bytes values
        manifest_struct_permissions = []
        for item in manifest_struct[5]:
            contract = item[0]

            from boa3.neo3.core.types import UInt160
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
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn({"contract": "*", "methods": "*"}, manifest['permissions'])

    def test_metadata_info_permissions_default(self):
        path = self.get_contract_path('MetadataInfoPermissionsDefault.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn({"contract": "*", "methods": "*"}, manifest['permissions'])

    def test_metadata_info_permissions_wildcard(self):
        path = self.get_contract_path('MetadataInfoPermissionsWildcard.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn({"contract": "*", "methods": "*"}, manifest['permissions'])

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

    def test_metadata_info_name(self):
        path = self.get_contract_path('MetadataInfoName.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('name', manifest)
        self.assertIsInstance(manifest['name'], str)
        self.assertGreater(len(manifest['name']), 0)
        self.assertEqual((manifest['name']), "SmartContractCustomName")

    def test_metadata_info_name_default(self):
        path = self.get_contract_path('MetadataInfoNameDefault.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('name', manifest)
        self.assertIsInstance(manifest['name'], str)
        self.assertGreater(len(manifest['name']), 0)
        self.assertEqual((manifest['name']), "MetadataInfoNameDefault")

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
                       'signature': '2p4uEy4pE3yj8jjmkhNrH3e0jI/w4WJCy3tTqlomSvCekM60tQ0zpmFfke+YOXa3tq/MlXLavqGUpNq/Pq3h5Q=='}, manifest['groups'])

        engine = TestEngine()
        # verify using NeoManifestStruct
        nef, manifest = self.get_bytes_output(path)
        self.run_smart_contract(engine, path, 'main')
        call_hash = engine.executed_script_hash.to_array()
        path = path.replace('.py', '.nef')

        get_contract_path = self.get_contract_path('test_sc/native_test/contractmanagement', 'GetContract.py')
        engine = TestEngine()
        engine.add_contract(path)

        result = self.run_smart_contract(engine, get_contract_path, 'main', call_hash)
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
        path = self.get_contract_path('MetadataInfoGroupsDefault.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('groups', manifest)
        self.assertIsInstance(manifest['groups'], list)
        self.assertEqual(len(manifest['groups']), 0)

    def test_metadata_info_source(self):
        path = self.get_contract_path('MetadataInfoSource.py')
        self.compile_and_save(path)

        nef_path = path.replace('.py', '.nef')
        with open(nef_path, mode='rb') as nef:
            from boa3.neo.contracts.neffile import NefFile
            generated_source = NefFile.deserialize(nef.read()).source

        self.assertEqual(generated_source, 'https://github.com/CityOfZion/neo3-boa')

    def test_metadata_info_source_default(self):
        path = self.get_contract_path('MetadataInfoSourceDefault.py')
        self.compile_and_save(path)

        nef_path = path.replace('.py', '.nef')
        with open(nef_path, mode='rb') as nef:
            from boa3.neo.contracts.neffile import NefFile
            generated_source = NefFile.deserialize(nef.read()).source

        self.assertEqual(generated_source, '')

    def test_metadata_info_source_mismatched_type(self):
        path = self.get_contract_path('MetadataInfoSourceMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
