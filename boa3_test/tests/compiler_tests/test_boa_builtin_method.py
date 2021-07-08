from boa3.exception import CompilerError
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestBuiltinMethod(BoaTest):

    default_folder: str = 'test_sc/boa_built_in_methods_test'

    def test_abort(self):
        path = self.get_contract_path('Abort.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', False)
        self.assertEqual(123, result)

        with self.assertRaises(TestExecutionException, msg=self.ABORTED_CONTRACT_MSG):
            self.run_smart_contract(engine, path, 'main', True)

    def test_deploy_def(self):
        path = self.get_contract_path('DeployDef.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'get_var')
        self.assertEqual(10, result)

    def test_deploy_def_incorrect_signature(self):
        path = self.get_contract_path('DeployDefWrongSignature.py')
        self.assertCompilerLogs(CompilerError.InternalIncorrectSignature, path)

    def test_will_not_compile(self):
        path = self.get_contract_path('WillNotCompile.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)
