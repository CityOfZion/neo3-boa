from boa3 import constants
from boa3.exception import CompilerError
from boa3.neo.cryptography import hash160
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine
from boa3_test.tests.test_classes.transactionattribute.oracleresponse import OracleResponseCode


class TestNativeContracts(BoaTest):
    default_folder: str = 'test_sc/interop_test/oracle'

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

        request_id = oracle_requests[0].arguments[0]
        with self.assertRaises(TestExecutionException):
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

        request_id = oracle_requests[0].arguments[0]
        with self.assertRaises(TestExecutionException):
            # callback function doesn't exist
            self.run_oracle_response(engine, request_id, OracleResponseCode.Success, b'12345')

    def test_import_interop_oracle_package(self):
        path = self.get_contract_path('ImportInteropOracle.py')
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

        request_id = oracle_requests[0].arguments[0]
        with self.assertRaises(TestExecutionException):
            # callback function doesn't exist
            self.run_oracle_response(engine, request_id, OracleResponseCode.Success, b'12345')

    def test_oracle_get_price(self):

        from boa3.model.builtin.interop.interop import Interop
        from boa3.neo3.contracts import CallFlags
        from boa3.model.builtin.interop.oracle.oraclegetpricemethod import OracleGetPriceMethod
        from boa3.constants import ORACLE_SCRIPT

        call_flags = Integer(CallFlags.ALL).to_byte_array(signed=True, min_length=1)
        method = String(OracleGetPriceMethod().method_name).to_bytes()

        expected_output = (
            Opcode.NEWARRAY0
            + Opcode.PUSHDATA1
            + Integer(len(call_flags)).to_byte_array(min_length=1, signed=True)
            + call_flags
            + Opcode.PUSHDATA1
            + Integer(len(method)).to_byte_array(min_length=1, signed=True)
            + method
            + Opcode.PUSHDATA1
            + Integer(len(ORACLE_SCRIPT)).to_byte_array(min_length=1, signed=True)
            + ORACLE_SCRIPT
            + Opcode.SYSCALL
            + Interop.CallContract.interop_method_hash
            + Opcode.RET
        )

        path = self.get_contract_path('OracleGetPrice.py')
        output, manifest = self.compile_and_save(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertIsInstance(result, int)
