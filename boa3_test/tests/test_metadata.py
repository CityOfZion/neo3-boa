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

        path = '%s/boa3_test/example/metadata_test/MetadataInfoMethod.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('features', manifest)
        self.assertIn('storage', manifest['features'])
        self.assertEqual(False, manifest['features']['storage'])
        self.assertIn('payable', manifest['features'])
        self.assertEqual(False, manifest['features']['payable'])

    def test_metadata_info_method_mismatched_type(self):
        path = '%s/boa3_test/example/metadata_test/MetadataInfoMethodMismatchedReturn.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_info_method_no_return(self):
        path = '%s/boa3_test/example/metadata_test/MetadataInfoMethodNoReturn.py' % self.dirname
        self.assertCompilerLogs(MissingReturnStatement, path)

    def test_metadata_info_multiple_method(self):
        expected_output = (
            Opcode.PUSH5        # return 5
            + Opcode.RET
        )

        path = '%s/boa3_test/example/metadata_test/MetadataInfoMultipleMethod.py' % self.dirname
        output = self.assertCompilerLogs(RedeclaredSymbol, path)
        self.assertEqual(expected_output, output)

    def test_metadata_info_storage(self):
        expected_output = (
            Opcode.PUSH5        # return 5
            + Opcode.RET
        )

        path = '%s/boa3_test/example/metadata_test/MetadataInfoStorage.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('features', manifest)
        self.assertIn('storage', manifest['features'])
        self.assertEqual(True, manifest['features']['storage'])

    def test_metadata_info_storage_mismatched_type(self):
        path = '%s/boa3_test/example/metadata_test/MetadataInfoStorageMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_info_payable(self):
        expected_output = (
            Opcode.PUSH5        # return 5
            + Opcode.RET
        )

        path = '%s/boa3_test/example/metadata_test/MetadataInfoPayable.py' % self.dirname
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        self.assertIn('features', manifest)
        self.assertIn('storage', manifest['features'])
        self.assertEqual(True, manifest['features']['payable'])

    def test_metadata_info_payable_mismatched_type(self):
        path = '%s/boa3_test/example/metadata_test/MetadataInfoPayableMismatchedType.py' % self.dirname
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_metadata_method_with_args(self):
        path = '%s/boa3_test/example/metadata_test/MetadataMethodWithArgs.py' % self.dirname
        self.assertCompilerLogs(UnexpectedArgument, path)

    def test_metadata_method_called_by_user_method(self):
        path = '%s/boa3_test/example/metadata_test/MetadataMethodCalledByUserMethod.py' % self.dirname
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_metadata_object_call_user_method(self):
        path = '%s/boa3_test/example/metadata_test/MetadataObjectCallUserMethod.py' % self.dirname
        self.assertCompilerLogs(UnresolvedReference, path)

    def test_metadata_object_type_user_method(self):
        path = '%s/boa3_test/example/metadata_test/MetadataObjectTypeUserMethod.py' % self.dirname
        self.assertCompilerLogs(UnresolvedReference, path)
