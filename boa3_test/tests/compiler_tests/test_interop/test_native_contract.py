from boa3 import constants
from boa3.exception.CompilerError import MismatchedTypes
from boa3.neo.cryptography import hash160
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestNativeContracts(BoaTest):

    default_folder: str = 'test_sc/interop_test/native_contracts'

    def test_oracle_request(self):
        path = self.get_contract_path('OracleRequestCall.py')
        output, manifest = self.compile_and_save(path)
        contract_script = hash160(output)

        engine = TestEngine()

        test_url = 'abc'
        request_filter = 'ABC'
        callback = '123'
        gas_for_response = 1_0000000
        result = self.run_smart_contract(engine, path, 'oracle_call',
                                         test_url, request_filter, callback, None, gas_for_response)
        self.assertIsVoid(result)

        oracle_requests = engine.get_events('OracleRequest', constants.ORACLE_SCRIPT)
        self.assertEqual(1, len(oracle_requests))
        self.assertEqual(4, len(oracle_requests[0].arguments))
        self.assertEqual(contract_script, oracle_requests[0].arguments[1])
        self.assertEqual(test_url, oracle_requests[0].arguments[2])
        self.assertEqual(request_filter, oracle_requests[0].arguments[3])

    def test_oracle_request_url_mismatched_type(self):
        path = self.get_contract_path('OracleRequestUrlMismatchedType.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_oracle_request_filter_mismatched_type(self):
        path = self.get_contract_path('OracleRequestFilterMismatchedType.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_oracle_request_callback_mismatched_type(self):
        path = self.get_contract_path('OracleRequestCallCallbackMismatchedType.py')
        self.assertCompilerLogs(MismatchedTypes, path)

    def test_oracle_request_gas_mismatched_type(self):
        path = self.get_contract_path('OracleRequestGasMismatchedType.py')
        self.assertCompilerLogs(MismatchedTypes, path)
