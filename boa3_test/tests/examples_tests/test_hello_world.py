from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestTemplate(BoaTest):
    default_folder: str = 'examples'

    def test_hello_world_compile(self):
        path = self.get_contract_path('hello_world.py')
        self.compile(path)

    def test_hello_world_main(self):
        path, _ = self.get_deploy_file_paths('hello_world.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'Main')

        hello_world_contract = invoke.invoke.contract
        runner.execute(get_storage_from=hello_world_contract)
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        self.assertIsNone(invoke.result)

        storage_result = runner.storages.get(hello_world_contract, b'hello')
        self.assertEqual(b'world', storage_result.as_bytes())
