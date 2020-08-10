from boa3.exception.CompilerError import (MetadataImplementationMissing, MetadataIncorrectImplementation,
                                          MismatchedTypes, MissingReturnStatement, UnexpectedArgument,
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
        self.assertIn('features', manifest)
        self.assertIn('storage', manifest['features'])
        self.assertEqual(False, manifest['features']['storage'])
        self.assertIn('payable', manifest['features'])
        self.assertEqual(False, manifest['features']['payable'])

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

    def test_metadata_info_storage(self):
        expected_output = (
            Opcode.PUSH5        # return 5
            + Opcode.RET
        )

        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoStorage.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('features', manifest)
        self.assertIn('storage', manifest['features'])
        self.assertEqual(True, manifest['features']['storage'])

    def test_metadata_info_storage_mismatched_type(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoStorageMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_info_payable(self):
        expected_output = (
            Opcode.PUSH5        # Main
            + Opcode.RET            # return 5
            + Opcode.PUSH0      # verify
            + Opcode.RET            # return False
        )

        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoPayable.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('features', manifest)
        self.assertIn('storage', manifest['features'])
        self.assertEqual(True, manifest['features']['payable'])

        self.assertIn('abi', manifest)
        self.assertIn('methods', manifest['abi'])
        self.assertTrue(any(method['name'] == 'verify' for method in manifest['abi']['methods'] if 'name' in method))

    def test_metadata_info_payable_mismatched_type(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoPayableMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_info_payable_missing_verify(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoPayableMissingVerify.py' % self.dirname
        self.assertCompilerLogs(MetadataImplementationMissing, path)

    def test_metadata_info_payable_incorrect_verify(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoPayableIncorrectVerify.py' % self.dirname
        self.assertCompilerLogs(MetadataIncorrectImplementation, path)

    def test_metadata_info_payable_private_verify(self):
        path = '%s/boa3_test/test_sc/metadata_test/MetadataInfoPayablePrivateVerify.py' % self.dirname
        self.assertCompilerLogs(MetadataIncorrectImplementation, path)

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
