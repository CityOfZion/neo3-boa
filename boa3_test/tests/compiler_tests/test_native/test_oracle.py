from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine
from boa3_test.tests.test_classes.transactionattribute.oracleresponse import OracleResponseCode


class TestNativeContracts(BoaTest):
    default_folder: str = 'test_sc/native_test/oracle'

    def test_get_hash(self):
        path = self.get_contract_path('GetHash.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual(constants.ORACLE_SCRIPT, result)

    def test_oracle_request(self):
        path = self.get_contract_path('OracleRequestCall.py')

        engine = TestEngine()

        test_url = 'abc'
        request_filter = 'ABC'
        callback = '123'
        gas_for_response = 1_0000000
        result = self.run_smart_contract(engine, path, 'oracle_call',
                                         test_url, request_filter, callback, None, gas_for_response)
        self.assertIsVoid(result)
        contract_script = engine.executed_script_hash.to_array()

        oracle_requests = engine.get_events('OracleRequest', constants.ORACLE_SCRIPT)
        self.assertEqual(1, len(oracle_requests))
        self.assertEqual(4, len(oracle_requests[0].arguments))
        self.assertEqual(contract_script, oracle_requests[0].arguments[1])
        self.assertEqual(test_url, oracle_requests[0].arguments[2])
        self.assertEqual(request_filter, oracle_requests[0].arguments[3])

        request_id = oracle_requests[0].arguments[0]
        with self.assertRaisesRegex(TestExecutionException, self.METHOD_DOESNT_EXIST_IN_CONTRACT_MSG_REGEX_PREFIX):
            # callback function doesn't exist
            self.run_oracle_response(engine, request_id, OracleResponseCode.Success, b'12345')

        test_url = 'abc'
        request_filter = 'ABC'
        callback = 'test_callback'
        gas_for_response = 1_0000000
        result = self.run_smart_contract(engine, path, 'oracle_call',
                                         test_url, request_filter, callback, None, gas_for_response)
        self.assertIsVoid(result)

        oracle_requests = engine.get_events('OracleRequest', constants.ORACLE_SCRIPT)
        self.assertEqual(2, len(oracle_requests))
        self.assertEqual(4, len(oracle_requests[1].arguments))

        request_id = oracle_requests[1].arguments[0]

        with self.assertRaises(TestExecutionException) as engine_exception:
            # TODO: remove this assertRaises when calling the native OracleContract is fixed
            result = self.run_oracle_response(engine, request_id, OracleResponseCode.Success, b'12345')
            self.assertIsVoid(result)

    def test_oracle_request_url_mismatched_type(self):
        path = self.get_contract_path('OracleRequestUrlMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_oracle_request_filter_mismatched_type(self):
        path = self.get_contract_path('OracleRequestFilterMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_oracle_request_callback_mismatched_type(self):
        path = self.get_contract_path('OracleRequestCallCallbackMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_oracle_request_gas_mismatched_type(self):
        path = self.get_contract_path('OracleRequestGasMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_import_interop_oracle(self):
        path = self.get_contract_path('ImportOracle.py')

        engine = TestEngine()

        test_url = 'abc'
        request_filter = 'ABC'
        callback = '123'
        gas_for_response = 1_0000000
        result = self.run_smart_contract(engine, path, 'oracle_call',
                                         test_url, request_filter, callback, None, gas_for_response)
        self.assertIsVoid(result)
        contract_script = engine.executed_script_hash.to_array()

        oracle_requests = engine.get_events('OracleRequest', constants.ORACLE_SCRIPT)
        self.assertEqual(1, len(oracle_requests))
        self.assertEqual(4, len(oracle_requests[0].arguments))
        self.assertEqual(contract_script, oracle_requests[0].arguments[1])
        self.assertEqual(test_url, oracle_requests[0].arguments[2])
        self.assertEqual(request_filter, oracle_requests[0].arguments[3])

        request_id = oracle_requests[0].arguments[0]
        with self.assertRaises(TestExecutionException):
            # callback function doesn't exist
            self.run_oracle_response(engine, request_id, OracleResponseCode.Success, b'12345')

    def test_import_interop_oracle_package(self):
        path = self.get_contract_path('ImportInteropOracle.py')

        engine = TestEngine()

        test_url = 'abc'
        request_filter = 'ABC'
        callback = '123'
        gas_for_response = 1_0000000
        result = self.run_smart_contract(engine, path, 'oracle_call',
                                         test_url, request_filter, callback, None, gas_for_response)
        self.assertIsVoid(result)
        contract_script = engine.executed_script_hash.to_array()

        oracle_requests = engine.get_events('OracleRequest', constants.ORACLE_SCRIPT)
        self.assertEqual(1, len(oracle_requests))
        self.assertEqual(4, len(oracle_requests[0].arguments))
        self.assertEqual(contract_script, oracle_requests[0].arguments[1])
        self.assertEqual(test_url, oracle_requests[0].arguments[2])
        self.assertEqual(request_filter, oracle_requests[0].arguments[3])

        request_id = oracle_requests[0].arguments[0]
        with self.assertRaises(TestExecutionException):
            # callback function doesn't exist
            self.run_oracle_response(engine, request_id, OracleResponseCode.Success, b'12345')

    def test_oracle_get_price(self):
        from boa3.internal.neo3.contracts import CallFlags
        from boa3.internal.model.builtin.interop.oracle.oraclegetpricemethod import OracleGetPriceMethod

        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        method = String(OracleGetPriceMethod().method_name).to_bytes()

        expected_output = (
            Opcode.CALLT + b'\x00\x00'
            + Opcode.RET
        )

        path = self.get_contract_path('OracleGetPrice.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertIsInstance(result, int)
