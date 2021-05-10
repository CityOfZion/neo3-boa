from boa3.exception.CompilerError import (MismatchedTypes, MissingReturnStatement, UnexpectedArgument,
                                          UnresolvedReference)
from boa3.exception.CompilerWarning import RedeclaredSymbol
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest


class TestMetadata(BoaTest):

    default_folder: str = 'test_sc/metadata_test'

    def test_metadata_info_method(self):
        expected_output = (
            Opcode.PUSH5        # return 5
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
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_info_method_no_return(self):
        path = self.get_contract_path('MetadataInfoMethodNoReturn.py')
        self.assertCompilerLogs(MissingReturnStatement, path)

    def test_metadata_info_multiple_method(self):
        expected_output = (
            Opcode.PUSH5        # return 5
            + Opcode.RET
        )

        path = self.get_contract_path('MetadataInfoMultipleMethod.py')
        self.assertCompilerLogs(RedeclaredSymbol, path)

        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('Description', manifest['extra'])
        self.assertEqual('func1', manifest['extra']['Description'])

    def test_metadata_method_with_args(self):
        path = self.get_contract_path('MetadataMethodWithArgs.py')
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_metadata_method_called_by_user_method(self):
        path = self.get_contract_path('MetadataMethodCalledByUserMethod.py')
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_metadata_object_call_user_method(self):
        path = self.get_contract_path('MetadataObjectCallUserMethod.py')
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_metadata_object_type_user_method(self):
        path = self.get_contract_path('MetadataObjectTypeUserMethod.py')
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_metadata_info_author(self):
        expected_output = (
            Opcode.PUSH5        # return 5
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
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_info_email(self):
        expected_output = (
            Opcode.PUSH5        # return 5
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
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_info_description(self):
        expected_output = (
            Opcode.PUSH5        # return 5
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
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_info_extras(self):
        expected_output = (
            Opcode.PUSH5        # return 5
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
            Opcode.PUSH5        # return 5
            + Opcode.RET
        )

        path = self.get_contract_path('MetadataInfoNewExtras.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)
        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('unittest1', manifest['extra'])
        self.assertEqual('string', manifest['extra']['unittest1'])
        self.assertIn('unittest2', manifest['extra'])
        self.assertEqual(123, manifest['extra']['unittest2'])
        self.assertIn('unittest3', manifest['extra'])
        self.assertEqual(True, manifest['extra']['unittest3'])
        self.assertIn('unittest4', manifest['extra'])
        self.assertEqual(['list', 3210], manifest['extra']['unittest4'])
