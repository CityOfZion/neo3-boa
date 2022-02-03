from boa3.constants import IMPORT_WILDCARD
from boa3.exception import CompilerError, CompilerWarning
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest


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
        self.assertIn('NEP-11', manifest['supportedstandards'])

    def test_metadata_info_supported_standards_missing_implementations(self):
        path = self.get_contract_path('MetadataInfoSupportedStandardsMissingImplementation.py')
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
        self.assertIn('030000123456789012345678901234567890123456789012345678901234abcdef', manifest['trusts'])
        self.assertIn('020000123456789012345678901234567890123456789012345678901234abcdef', manifest['trusts'])

    def test_metadata_info_trusts_wildcard(self):
        path = self.get_contract_path('MetadataInfoTrustsWildcard.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('trusts', manifest)
        self.assertIsInstance(manifest['trusts'], list)
        self.assertEqual(len(manifest['trusts']), 1)
        self.assertIn(IMPORT_WILDCARD, manifest['trusts'])

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

    def test_metadata_info_permissions_Wildcard(self):
        path = self.get_contract_path('MetadataInfoPermissionsWildcard.py')
        output, manifest = self.compile_and_save(path)

        self.assertIn('permissions', manifest)
        self.assertIsInstance(manifest['permissions'], list)
        self.assertEqual(len(manifest['permissions']), 1)
        self.assertIn({"contract": "*", "methods": "*"}, manifest['permissions'])

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
