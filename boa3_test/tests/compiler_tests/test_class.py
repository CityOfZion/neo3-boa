from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.exception import CompilerError
from boa3.internal.exception.NotLoadedException import NotLoadedException
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.tests.test_drive.testrunner.boa_test_runner import BoaTestRunner


class TestClass(BoaTest):
    default_folder: str = 'test_sc/class_test'

    def test_notification_get_variables(self):
        path, _ = self.get_deploy_file_paths('NotificationGetVariables.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        contract_invoke = runner.call_contract(path, 'script_hash', [],
                                               expected_result_type=bytes)
        invokes.append(contract_invoke)
        expected_results.append(bytes(20))

        runner.update_contracts(export_checkpoint=True)
        script = contract_invoke.invoke.contract.script_hash

        invokes.append(runner.call_contract(path, 'event_name', []))
        expected_results.append('')

        invokes.append(runner.call_contract(path, 'state', []))
        expected_results.append([])

        invokes.append(runner.call_contract(path, 'script_hash', [1]))
        expected_results.append(script)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        contract_notifications = runner.get_events(origin=script)
        self.assertEqual(len(contract_notifications), 1)

        invokes.append(runner.call_contract(path, 'event_name', [1]))
        expected_results.append('notify')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        contract_notifications = runner.get_events(origin=script)
        self.assertEqual(len(contract_notifications), 1)

        invokes.append(runner.call_contract(path, 'state', [1]))
        expected_results.append([1])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        contract_notifications = runner.get_events(origin=script)
        self.assertEqual(len(contract_notifications), 1)

        invokes.append(runner.call_contract(path, 'state', ['1']))
        expected_results.append(['1'])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        contract_notifications = runner.get_events(origin=script)
        self.assertEqual(len(contract_notifications), 1)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_notification_set_variables(self):
        path, _ = self.get_deploy_file_paths('NotificationSetVariables.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        contract_invoke = runner.call_contract(path, 'script_hash', b'',
                                               expected_result_type=bytes)
        invokes.append(contract_invoke)
        expected_results.append(b'')

        runner.update_contracts(export_checkpoint=True)
        script = contract_invoke.invoke.contract.script_hash

        invokes.append(runner.call_contract(path, 'script_hash', script,
                                            expected_result_type=bytes))
        expected_results.append(script)

        invokes.append(runner.call_contract(path, 'event_name', 'unit test'))
        expected_results.append('unit test')

        invokes.append(runner.call_contract(path, 'state', (1, 2, 3)))
        expected_results.append([1, 2, 3])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_contract_constructor(self):
        path, _ = self.get_deploy_file_paths('ContractConstructor.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invoke = runner.call_contract(path, 'new_contract')
        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        result = invoke.result
        self.assertEqual(5, len(result))

        if isinstance(result[2], str):
            result[2] = String(result[2]).to_bytes()
        if isinstance(result[3], str):
            result[3] = String(result[3]).to_bytes()

        self.assertEqual(0, result[0])
        self.assertEqual(0, result[1])
        self.assertEqual(bytes(20), result[2])
        self.assertEqual(bytes(), result[3])
        self.assertEqual({}, result[4])

    def test_user_class_empty(self):
        # since 0.11.2 methods that are not public nor are called are not generated to optimize code
        # this test generates an empty contract
        path = self.get_contract_path('UserClassEmpty.py')

        with self.assertRaises(NotLoadedException) as e:
            output = self.compile(path)

        self.assertTrue(e.exception.empty_script)

    def test_user_class_with_static_method_from_class(self):
        path, _ = self.get_deploy_file_paths('UserClassWithStaticMethodFromClass.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_by_class_name'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_static_method_from_class_with_same_method_name(self):
        path, _ = self.get_deploy_file_paths('UserClassWithStaticMethodFromClassWithSameNameMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_by_class_name'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_static_method_from_object(self):
        path = self.get_contract_path('UserClassWithStaticMethodFromObject.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_user_class_with_static_method_with_args(self):
        path, _ = self.get_deploy_file_paths('UserClassWithStaticMethodWithArgs.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_by_class_name', 10, 10))
        expected_results.append(30)

        invokes.append(runner.call_contract(path, 'call_by_class_name', 30, -30))
        expected_results.append(10)

        invokes.append(runner.call_contract(path, 'call_by_class_name', -5, -10))
        expected_results.append(-5)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_static_method_with_vararg(self):
        path, _ = self.get_deploy_file_paths('UserClassWithStaticMethodWithVararg.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_by_class_name', []))
        expected_results.append(42)

        args = [1, 2, 3]
        invokes.append(runner.call_contract(path, 'call_by_class_name', args))
        expected_results.append(args[0])

        args = [4, 3, 2, 1]
        invokes.append(runner.call_contract(path, 'call_by_class_name', args))
        expected_results.append(args[0])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_static_method_not_class_method(self):
        path, _ = self.get_deploy_file_paths('UserClassWithStaticMethodNotClassMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_by_class_name', 42))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_class_method_called_from_class_name(self):
        path, _ = self.get_deploy_file_paths('UserClassWithClassMethodFromClass.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_by_class_name'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_class_method_called_from_object(self):
        path, _ = self.get_deploy_file_paths('UserClassWithClassMethodFromObject.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_by_class_name'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_class_method_called_from_variable(self):
        path, _ = self.get_deploy_file_paths('UserClassWithClassMethodFromVariable.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_by_class_name'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_class_method_with_args(self):
        path, _ = self.get_deploy_file_paths('UserClassWithClassMethodWithArgs.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_by_class_name', 42))
        expected_results.append(42)

        invokes.append(runner.call_contract(path, 'call_by_class_name', 1))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'call_by_class_name', -10))
        expected_results.append(-10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_class_method_with_vararg(self):
        path, _ = self.get_deploy_file_paths('UserClassWithClassMethodWithVararg.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_by_class_name', []))
        expected_results.append(42)

        args = [1, 2, 3]
        invokes.append(runner.call_contract(path, 'call_by_class_name', args))
        expected_results.append(args[0])

        args = [4, 3, 2, 1]
        invokes.append(runner.call_contract(path, 'call_by_class_name', args))
        expected_results.append(args[0])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_class_variable_from_class(self):
        path, _ = self.get_deploy_file_paths('UserClassWithClassVariableFromClass.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_val1'))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'get_val2'))
        expected_results.append(2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_class_variable_from_object(self):
        path, _ = self.get_deploy_file_paths('UserClassWithClassVariableFromObject.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_val1'))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'get_val2'))
        expected_results.append(2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_class_variable_from_variable(self):
        path, _ = self.get_deploy_file_paths('UserClassWithClassVariableFromVariable.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_val1'))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'get_val2'))
        expected_results.append(2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_update_class_variable(self):
        path = self.get_contract_path('UserClassUpdateClassVariable.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_user_class_update_instance_variable_on_init(self):
        path = self.get_contract_path('UserClassUpdateClassVariableOnInit.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_user_class_with_class_variable_and_class_method(self):
        path, _ = self.get_deploy_file_paths('UserClassWithClassVariableAndClassMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_val1'))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'get_foo'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_init(self):
        path, _ = self.get_deploy_file_paths('UserClassWithInit.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'build_example_object'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_init_with_args(self):
        path, _ = self.get_deploy_file_paths('UserClassWithInitWithArgs.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'build_example_object'))
        expected_results.append([])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_instance_method(self):
        path, _ = self.get_deploy_file_paths('UserClassWithInstanceMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_by_class_name'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_instance_method_from_variable(self):
        path, _ = self.get_deploy_file_paths('UserClassWithInstanceMethodFromVariable.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'call_by_class_name'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_instance_method_from_class(self):
        path = self.get_contract_path('UserClassWithInstanceMethodFromClass.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_user_class_with_instance_variable_from_class(self):
        path = self.get_contract_path('UserClassWithInstanceVariableFromClass.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_user_class_with_instance_variable_from_object(self):
        path, _ = self.get_deploy_file_paths('UserClassWithInstanceVariableFromObject.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_val1'))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'get_val2'))
        expected_results.append(2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_instance_variable_from_variable(self):
        path, _ = self.get_deploy_file_paths('UserClassWithInstanceVariableFromVariable.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_val1'))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'get_val2'))
        expected_results.append(2)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_update_instance_variable(self):
        path, _ = self.get_deploy_file_paths('UserClassUpdateInstanceVariable.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_val', 10))
        expected_results.append([10, 10, 2])

        invokes.append(runner.call_contract(path, 'get_val', 40))
        expected_results.append([10, 40, 2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_access_variable_on_init(self):
        path, _ = self.get_deploy_file_paths('UserClassAccessInstanceVariableOnInit.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_obj'))
        expected_results.append([2, 4])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_access_variable_on_method(self):
        path, _ = self.get_deploy_file_paths('UserClassAccessInstanceVariableOnMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_val1'))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'get_val2'))
        expected_results.append(4)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_base(self):
        path = self.get_contract_path('UserClassWithBuiltinBase.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_user_class_with_created_base(self):
        path, _ = self.get_deploy_file_paths('UserClassWithCreatedBase.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'implemented_method'))
        expected_results.append(42)

        invokes.append(runner.call_contract(path, 'inherited_method'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_cascated_created_base(self):
        path, _ = self.get_deploy_file_paths('UserClassWithCascadeCreatedBase.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'implemented_method'))
        expected_results.append(42)

        invokes.append(runner.call_contract(path, 'inherited_method'))
        expected_results.append(42)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_created_base_with_variable(self):
        path, _ = self.get_deploy_file_paths('UserClassWithCreatedBaseWithVariables.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'implemented_variable'))
        expected_results.append(42)

        invokes.append(runner.call_contract(path, 'inherited_variable'))
        expected_results.append(42)

        new_value = 10
        invokes.append(runner.call_contract(path, 'update_variable', new_value))
        expected_results.append(new_value)

        new_value = -10
        invokes.append(runner.call_contract(path, 'update_variable', new_value))
        expected_results.append(new_value)

        new_value = 10_000_000
        invokes.append(runner.call_contract(path, 'update_variable', new_value))
        expected_results.append(new_value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_created_base_with_args(self):
        path, _ = self.get_deploy_file_paths('UserClassWithCreatedBaseWithArgs.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        init_value = 42
        invokes.append(runner.call_contract(path, 'implemented_var', init_value))
        expected_results.append(init_value)

        invokes.append(runner.call_contract(path, 'inherited_var', init_value))
        expected_results.append(init_value)

        init_value = -42
        invokes.append(runner.call_contract(path, 'implemented_var', init_value))
        expected_results.append(init_value)

        invokes.append(runner.call_contract(path, 'inherited_var', init_value))
        expected_results.append(init_value)

        init_value = 10_000_000
        invokes.append(runner.call_contract(path, 'implemented_var', init_value))
        expected_results.append(init_value)

        invokes.append(runner.call_contract(path, 'inherited_var', init_value))
        expected_results.append(init_value)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_created_base_with_init(self):
        path, _ = self.get_deploy_file_paths('UserClassWithCreatedBaseWithInit.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = 42
        invokes.append(runner.call_contract(path, 'inherited_var'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_created_base_with_init_with_args(self):
        path, _ = self.get_deploy_file_paths('UserClassWithCreatedBaseWithInitWithArgs.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = -10
        invokes.append(runner.call_contract(path, 'inherited_var'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_created_base_with_more_variables(self):
        path, _ = self.get_deploy_file_paths('UserClassWithCreatedBaseWithMoreVariables.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        expected_result = [42, 10, 20]
        invokes.append(runner.call_contract(path, 'get_full_object'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_created_base_with_more_variables_without_super_init(self):
        path = self.get_contract_path('UserClassWithCreatedBaseWithMoreVariablesWithoutSuperInit.py')
        self.assertCompilerLogs(CompilerError.MissingInitCall, path)

    def test_user_class_with_multiple_bases(self):
        path = self.get_contract_path('UserClassWithMultipleBases.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_user_class_with_keyword_base(self):
        path = self.get_contract_path('UserClassWithKeywordBase.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_user_class_with_decorator(self):
        path = self.get_contract_path('UserClassWithDecorator.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_user_class_with_property_from_object(self):
        path, _ = self.get_deploy_file_paths('UserClassWithPropertyFromObject.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_property'))
        expected_results.append(1)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_property_using_instance_variables_from_object(self):
        path, _ = self.get_deploy_file_paths('UserClassWithPropertyUsingInstanceVariablesFromObject.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_property'))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_property_using_class_variables_from_object(self):
        path, _ = self.get_deploy_file_paths('UserClassWithPropertyUsingClassVariablesFromObject.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_property'))
        expected_results.append(10)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_property_using_variables_from_object(self):
        path, _ = self.get_deploy_file_paths('UserClassWithPropertyUsingVariablesFromObject.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_property'))
        expected_results.append(47)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_property_from_class(self):
        path = self.get_contract_path('UserClassWithPropertyFromClass.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_user_class_with_property_using_arguments(self):
        path = self.get_contract_path('UserClassWithPropertyUsingArguments.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_user_class_with_property_mismatched_type(self):
        path = self.get_contract_path('UserClassWithPropertyMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)

    def test_user_class_with_property_without_self(self):
        path = self.get_contract_path('UserClassWithPropertyWithoutSelf.py')
        self.assertCompilerLogs(CompilerError.SelfArgumentError, path)

    def test_user_class_with_augmented_assignment_operator_with_variable(self):
        path, _ = self.get_deploy_file_paths('UserClassWithAugmentedAssignmentOperatorWithVariable.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'add'))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'sub'))
        expected_results.append(-2)

        invokes.append(runner.call_contract(path, 'mult'))
        expected_results.append(16)

        invokes.append(runner.call_contract(path, 'div'))
        expected_results.append(2)

        invokes.append(runner.call_contract(path, 'mod'))
        expected_results.append(1)

        invokes.append(runner.call_contract(path, 'mix'))
        expected_results.append(0)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_user_class_with_deploy_method(self):
        path, _ = self.get_deploy_file_paths('UserClassWithDeployMethod.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'get_obj'))
        expected_results.append([1, 2])

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_del_class(self):
        path = self.get_contract_path('DelClass.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_class_property_and_parameter_with_same_name(self):
        path, _ = self.get_deploy_file_paths('ClassPropertyAndParameterWithSameName.py')
        runner = BoaTestRunner(runner_id=self.method_name())

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'unit test'))
        expected_results.append('unit test')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state, msg=runner.error)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)
