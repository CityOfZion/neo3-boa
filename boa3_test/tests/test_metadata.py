from boa3.exception.CompilerError import (MismatchedTypes, MissingReturnStatement, UnexpectedArgument,
                                          UnresolvedReference)
from boa3.exception.CompilerWarning import RedeclaredSymbol
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest


class TestMetadata(BoaTest):

    def test_metadata_info_method(self):
        expected_output = (
            Opcode.PUSH5        # return 5
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoMethod.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        # test features fields
        # removed in neo3-preview4
        self.assertNotIn('features', manifest)

        # test extra field
        self.assertIn('extra', manifest)
        self.assertIsNone(manifest['extra'])

    def test_metadata_info_method_mismatched_type(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoMethodMismatchedReturn.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_info_method_no_return(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoMethodNoReturn.py' % self.dirname
        self.assertCompilerLogs(MissingReturnStatement, path)

    def test_metadata_info_multiple_method(self):
        expected_output = (
            Opcode.PUSH5        # return 5
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoMultipleMethod.py' % self.dirname
        self.assertCompilerLogs(RedeclaredSymbol, path)

        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('Description', manifest['extra'])
        self.assertEqual('func1', manifest['extra']['Description'])

    def test_metadata_method_with_args(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataMethodWithArgs.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_metadata_method_called_by_user_method(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataMethodCalledByUserMethod.py' % self.dirname
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_metadata_object_call_user_method(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataObjectCallUserMethod.py' % self.dirname
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_metadata_object_type_user_method(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataObjectTypeUserMethod.py' % self.dirname
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_metadata_info_author(self):
        expected_output = (
            Opcode.PUSH5        # return 5
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoAuthor.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('Author', manifest['extra'])
        self.assertEqual('Test', manifest['extra']['Author'])

    def test_metadata_info_author_mismatched_type(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoAuthorMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_info_email(self):
        expected_output = (
            Opcode.PUSH5        # return 5
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoEmail.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('Email', manifest['extra'])
        self.assertEqual('test@test.com', manifest['extra']['Email'])

    def test_metadata_info_email_mismatched_type(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoEmailMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_info_description(self):
        expected_output = (
            Opcode.PUSH5        # return 5
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoDescription.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('extra', manifest)
        self.assertIsNotNone(manifest['extra'])
        self.assertIn('Description', manifest['extra'])
        self.assertEqual('This is an example', manifest['extra']['Description'])

    def test_metadata_info_description_mismatched_type(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoDescriptionMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_info_extras(self):
        expected_output = (
            Opcode.PUSH5        # return 5
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoExtras.py' % self.dirname
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
