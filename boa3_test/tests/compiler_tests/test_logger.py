from boa3_test.tests import boatestcase


class TestImport(boatestcase.BoaTestCase):
    def test_log_multiple_errors_on_import(self):
        path = self.get_contract_path('test_sc/import_test', 'ImportFailInnerNotExistingMethod.py')
        errors, _ = self.get_all_compile_log_data(path, fail_fast=False)
        self.assertGreater(len(errors), 1)

    def test_log_fail_fast_error_on_import(self):
        path = self.get_contract_path('test_sc/import_test', 'ImportFailInnerNotExistingMethod.py')
        errors, _ = self.get_all_compile_log_data(path, fail_fast=True)
        self.assertEqual(1, len(errors))
