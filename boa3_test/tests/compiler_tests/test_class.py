from boa3.boa3 import Boa3
from boa3.exception import CompilerError
from boa3.neo.cryptography import hash160
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestClass(BoaTest):

    default_folder: str = 'test_sc/class_test'

    def test_notification_get_variables(self):
        path = self.get_contract_path('NotificationGetVariables.py')
        output, manifest = self.compile_and_save(path)

        script = hash160(output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'script_hash', [],
                                         expected_result_type=bytes)
        contract_notifications = engine.get_events(origin=script)
        self.assertEqual(len(contract_notifications), 0)
        self.assertEqual(bytes(20), result)

        result = self.run_smart_contract(engine, path, 'event_name', [])
        contract_notifications = engine.get_events(origin=script)
        self.assertEqual(len(contract_notifications), 0)
        self.assertEqual('', result)

        result = self.run_smart_contract(engine, path, 'state', [])
        contract_notifications = engine.get_events(origin=script)
        self.assertEqual(len(contract_notifications), 0)
        self.assertEqual([], result)

        result = self.run_smart_contract(engine, path, 'script_hash', [1])
        contract_notifications = engine.get_events(origin=script)
        self.assertEqual(len(contract_notifications), 1)
        self.assertEqual(script, result)

        engine.reset_engine()
        result = self.run_smart_contract(engine, path, 'event_name', [1])
        contract_notifications = engine.get_events(origin=script)
        self.assertEqual(len(contract_notifications), 1)
        self.assertEqual('notify', result)

        engine.reset_engine()
        result = self.run_smart_contract(engine, path, 'state', [1])
        contract_notifications = engine.get_events(origin=script)
        self.assertEqual(len(contract_notifications), 1)
        self.assertEqual([1], result)

        engine.reset_engine()
        result = self.run_smart_contract(engine, path, 'state', ['1'])
        contract_notifications = engine.get_events(origin=script)
        self.assertEqual(len(contract_notifications), 1)
        self.assertEqual(['1'], result)

    def test_notification_set_variables(self):
        path = self.get_contract_path('NotificationSetVariables.py')
        output, manifest = self.compile_and_save(path)

        script = hash160(output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'script_hash', script,
                                         expected_result_type=bytes)
        self.assertEqual(script, result)

        result = self.run_smart_contract(engine, path, 'event_name', 'unit test')
        self.assertEqual('unit test', result)

        result = self.run_smart_contract(engine, path, 'state', (1, 2, 3))
        self.assertEqual([1, 2, 3], result)

    def test_contract_constructor(self):
        path = self.get_contract_path('ContractConstructor.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'new_contract')
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
        path = self.get_contract_path('UserClassEmpty.py')
        output = Boa3.compile(path)

        self.assertEqual(b'', output)

    def test_user_class_with_static_method_from_class(self):
        path = self.get_contract_path('UserClassWithStaticMethodFromClass.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'call_by_class_name')
        self.assertEqual(42, result)

    def test_user_class_with_static_method_from_class_with_same_method_name(self):
        path = self.get_contract_path('UserClassWithStaticMethodFromClassWithSameNameMethod.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'call_by_class_name')
        self.assertEqual(42, result)

    def test_user_class_with_static_method_from_object(self):
        path = self.get_contract_path('UserClassWithStaticMethodFromObject.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_user_class_with_static_method_with_args(self):
        path = self.get_contract_path('UserClassWithStaticMethodWithArgs.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'call_by_class_name', 10, 10)
        self.assertEqual(30, result)

        result = self.run_smart_contract(engine, path, 'call_by_class_name', 30, -30)
        self.assertEqual(10, result)

        result = self.run_smart_contract(engine, path, 'call_by_class_name', -5, -10)
        self.assertEqual(-5, result)

    def test_user_class_with_static_method_with_vararg(self):
        path = self.get_contract_path('UserClassWithStaticMethodWithVararg.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'call_by_class_name', [])
        self.assertEqual(42, result)

        args = [1, 2, 3]
        result = self.run_smart_contract(engine, path, 'call_by_class_name', args)
        self.assertEqual(args[0], result)

        args = [4, 3, 2, 1]
        result = self.run_smart_contract(engine, path, 'call_by_class_name', args)
        self.assertEqual(args[0], result)

    def test_user_class_with_static_method_not_class_method(self):
        path = self.get_contract_path('UserClassWithStaticMethodNotClassMethod.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'call_by_class_name', 42)
        self.assertEqual(42, result)

    def test_user_class_with_class_method_called_from_class_name(self):
        path = self.get_contract_path('UserClassWithClassMethodFromClass.py')
        self.compile_and_save(path)
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'call_by_class_name')
        self.assertEqual(42, result)

    def test_user_class_with_class_method_called_from_object(self):
        path = self.get_contract_path('UserClassWithClassMethodFromObject.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'call_by_class_name')
        self.assertEqual(42, result)

    def test_user_class_with_class_method_with_args(self):
        path = self.get_contract_path('UserClassWithClassMethodWithArgs.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'call_by_class_name', 42)
        self.assertEqual(42, result)

        result = self.run_smart_contract(engine, path, 'call_by_class_name', 1)
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'call_by_class_name', -10)
        self.assertEqual(-10, result)

    def test_user_class_with_class_method_with_vararg(self):
        path = self.get_contract_path('UserClassWithClassMethodWithVararg.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'call_by_class_name', [])
        self.assertEqual(42, result)

        args = [1, 2, 3]
        result = self.run_smart_contract(engine, path, 'call_by_class_name', args)
        self.assertEqual(args[0], result)

        args = [4, 3, 2, 1]
        result = self.run_smart_contract(engine, path, 'call_by_class_name', args)
        self.assertEqual(args[0], result)

    def test_user_class_with_class_variable_from_class(self):
        path = self.get_contract_path('UserClassWithClassVariableFromClass.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'get_val1')
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'get_val2')
        self.assertEqual(2, result)

    def test_user_class_with_class_variable_from_object(self):
        path = self.get_contract_path('UserClassWithClassVariableFromObject.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'get_val1')
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'get_val2')
        self.assertEqual(2, result)

    def test_user_class_update_class_variable(self):
        path = self.get_contract_path('UserClassUpdateClassVariable.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_user_class_with_class_variable_and_class_method(self):
        path = self.get_contract_path('UserClassWithClassVariableAndClassMethod.py')
        self.compile_and_save(path)
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'get_val1')
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'get_foo')
        self.assertEqual(42, result)

    def test_user_class_with_init(self):
        path = self.get_contract_path('UserClassWithInit.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'build_example_object')
        self.assertEqual([], result)

    def test_user_class_with_init_with_args(self):
        path = self.get_contract_path('UserClassWithInitWithArgs.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'build_example_object')
        self.assertEqual([], result)

    def test_user_class_with_instance_method(self):
        path = self.get_contract_path('UserClassWithInstanceMethod.py')
        self.compile_and_save(path)
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'call_by_class_name')
        self.assertEqual(42, result)

    def test_user_class_with_instance_variable_from_class(self):
        path = self.get_contract_path('UserClassWithInstanceVariableFromClass.py')
        self.assertCompilerLogs(CompilerError.UnresolvedReference, path)

    def test_user_class_with_instance_variable_from_object(self):
        path = self.get_contract_path('UserClassWithInstanceVariableFromObject.py')
        self.compile_and_save(path)
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'get_val1')
        self.assertEqual(1, result)

        result = self.run_smart_contract(engine, path, 'get_val2')
        self.assertEqual(2, result)

    def test_user_class_update_instance_variable(self):
        path = self.get_contract_path('UserClassUpdateInstanceVariable.py')
        self.compile_and_save(path)
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'get_val', 10)
        self.assertEqual([10, 2], result)

        result = self.run_smart_contract(engine, path, 'get_val', 40)
        self.assertEqual([40, 2], result)

    def test_user_class_with_base(self):
        path = self.get_contract_path('UserClassWithBase.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_user_class_with_keyword_base(self):
        path = self.get_contract_path('UserClassWithKeywordBase.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)

    def test_user_class_with_decorator(self):
        path = self.get_contract_path('UserClassWithDecorator.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)
