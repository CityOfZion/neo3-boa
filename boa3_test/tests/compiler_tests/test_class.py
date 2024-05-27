from neo3.core import types

from boa3.internal.exception import CompilerError
from boa3.internal.exception.NotLoadedException import NotLoadedException
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestClass(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/class_test'

    async def test_notification_get_variables(self):
        await self.set_up_contract('NotificationGetVariables.py')

        script = self.contract_hash
        result, _ = await self.call('event_name', [[]], return_type=str)
        self.assertEqual('', result)

        result, _ = await self.call('state', [[]], return_type=list)
        self.assertEqual([], result)

        result, events = await self.call('script_hash', [[1]], return_type=types.UInt160)
        self.assertEqual(script, result)
        self.assertEqual(len(events), 1)

        result, events = await self.call('event_name', [[1]], return_type=str)
        self.assertEqual('notify', result)
        self.assertEqual(len(events), 1)

        result, events = await self.call('state', [[1]], return_type=list)
        self.assertEqual([1], result)
        self.assertEqual(len(events), 1)

        result, events = await self.call('state', [['1']], return_type=list[str])
        self.assertEqual(['1'], result)
        self.assertEqual(len(events), 1)

    async def test_notification_set_variables(self):
        await self.set_up_contract('NotificationSetVariables.py')

        script = self.contract_hash
        result, _ = await self.call('script_hash', [script], return_type=types.UInt160)
        self.assertEqual(script, result)

        result, _ = await self.call('event_name', ['unit test'], return_type=str)
        self.assertEqual('unit test', result)

        result, _ = await self.call('state', [(1, 2, 3)], return_type=list)
        self.assertEqual([1, 2, 3], result)

    async def test_contract_constructor(self):
        await self.set_up_contract('ContractConstructor.py')

        result, _ = await self.call('new_contract', return_type=list)
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

    async def test_user_class_with_static_method_from_class(self):
        await self.set_up_contract('UserClassWithStaticMethodFromClass.py')

        result, _ = await self.call('call_by_class_name', [], return_type=int)
        self.assertEqual(42, result)

    async def test_user_class_with_static_method_from_class_with_same_method_name(self):
        await self.set_up_contract('UserClassWithStaticMethodFromClassWithSameNameMethod.py')

        result, _ = await self.call('call_by_class_name', [], return_type=int)
        self.assertEqual(42, result)

    def test_user_class_with_static_method_from_object(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'UserClassWithStaticMethodFromObject.py')

    async def test_user_class_with_static_method_with_args(self):
        await self.set_up_contract('UserClassWithStaticMethodWithArgs.py')

        result, _ = await self.call('call_by_class_name', [10, 10], return_type=int)
        self.assertEqual(30, result)

        result, _ = await self.call('call_by_class_name', [30, -30], return_type=int)
        self.assertEqual(10, result)

        result, _ = await self.call('call_by_class_name', [-5, -10], return_type=int)
        self.assertEqual(-5, result)

    async def test_user_class_with_static_method_with_vararg(self):
        await self.set_up_contract('UserClassWithStaticMethodWithVararg.py')

        result, _ = await self.call('call_by_class_name', [[]], return_type=int)
        self.assertEqual(42, result)

        args = [1, 2, 3]
        result, _ = await self.call('call_by_class_name', [args], return_type=int)
        self.assertEqual(args[0], result)

        args = [4, 3, 2, 1]
        result, _ = await self.call('call_by_class_name', [args], return_type=int)
        self.assertEqual(args[0], result)

    async def test_user_class_with_static_method_not_class_method(self):
        await self.set_up_contract('UserClassWithStaticMethodNotClassMethod.py')

        result, _ = await self.call('call_by_class_name', [42], return_type=int)
        self.assertEqual(42, result)

    async def test_user_class_with_class_method_called_from_class_name(self):
        await self.set_up_contract('UserClassWithClassMethodFromClass.py')

        result, _ = await self.call('call_by_class_name', [], return_type=int)
        self.assertEqual(42, result)

    async def test_user_class_with_class_method_called_from_object(self):
        await self.set_up_contract('UserClassWithClassMethodFromObject.py')

        result, _ = await self.call('call_by_class_name', [], return_type=int)
        self.assertEqual(42, result)

    async def test_user_class_with_class_method_called_from_variable(self):
        await self.set_up_contract('UserClassWithClassMethodFromVariable.py')

        result, _ = await self.call('call_by_class_name', [], return_type=int)
        self.assertEqual(42, result)

    async def test_user_class_with_class_method_with_args(self):
        await self.set_up_contract('UserClassWithClassMethodWithArgs.py')

        result, _ = await self.call('call_by_class_name', [42], return_type=int)
        self.assertEqual(42, result)

        result, _ = await self.call('call_by_class_name', [1], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('call_by_class_name', [-10], return_type=int)
        self.assertEqual(-10, result)

    async def test_user_class_with_class_method_with_vararg(self):
        await self.set_up_contract('UserClassWithClassMethodWithVararg.py')

        result, _ = await self.call('call_by_class_name', [[]], return_type=int)
        self.assertEqual(42, result)

        args = [1, 2, 3]
        result, _ = await self.call('call_by_class_name', [args], return_type=int)
        self.assertEqual(args[0], result)

        args = [4, 3, 2, 1]
        result, _ = await self.call('call_by_class_name', [args], return_type=int)
        self.assertEqual(args[0], result)

    async def test_user_class_with_class_variable_from_class(self):
        await self.set_up_contract('UserClassWithClassVariableFromClass.py')

        result, _ = await self.call('get_val1', [], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('get_val2', [], return_type=int)
        self.assertEqual(2, result)

    async def test_user_class_with_class_variable_from_object(self):
        await self.set_up_contract('UserClassWithClassVariableFromObject.py')

        result, _ = await self.call('get_val1', [], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('get_val2', [], return_type=int)
        self.assertEqual(2, result)

    async def test_user_class_with_class_variable_from_variable(self):
        await self.set_up_contract('UserClassWithClassVariableFromVariable.py')

        result, _ = await self.call('get_val1', [], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('get_val2', [], return_type=int)
        self.assertEqual(2, result)

    def test_user_class_update_class_variable(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'UserClassUpdateClassVariable.py')

    def test_user_class_update_instance_variable_on_init(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'UserClassUpdateClassVariableOnInit.py')

    async def test_user_class_with_class_variable_and_class_method(self):
        await self.set_up_contract('UserClassWithClassVariableAndClassMethod.py')

        result, _ = await self.call('get_val1', [], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('get_foo', [], return_type=int)
        self.assertEqual(42, result)

    async def test_user_class_with_init(self):
        await self.set_up_contract('UserClassWithInit.py')
        from boa3_test.test_sc.class_test.UserClassWithInit import Example

        result, _ = await self.call('build_example_object', [], return_type=list)
        self.assertObjectEqual(Example(), result)

    async def test_user_class_with_init_with_args(self):
        await self.set_up_contract('UserClassWithInitWithArgs.py')
        from boa3_test.test_sc.class_test.UserClassWithInitWithArgs import Example

        result, _ = await self.call('build_example_object', [], return_type=list)
        self.assertObjectEqual(Example(42, '42'), result)

    async def test_user_class_with_instance_method(self):
        await self.set_up_contract('UserClassWithInstanceMethod.py')

        result, _ = await self.call('call_by_class_name', [], return_type=int)
        self.assertEqual(42, result)

    async def test_user_class_with_instance_method_from_variable(self):
        await self.set_up_contract('UserClassWithInstanceMethodFromVariable.py')

        result, _ = await self.call('call_by_class_name', [], return_type=int)
        self.assertEqual(42, result)

    def test_user_class_with_instance_method_from_class(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'UserClassWithInstanceMethodFromClass.py')

    def test_user_class_with_instance_variable_from_class(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'UserClassWithInstanceVariableFromClass.py')

    async def test_user_class_with_instance_variable_from_object(self):
        await self.set_up_contract('UserClassWithInstanceVariableFromObject.py')

        result, _ = await self.call('get_val1', [], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('get_val2', [], return_type=int)
        self.assertEqual(2, result)

    async def test_user_class_with_instance_variable_from_variable(self):
        await self.set_up_contract('UserClassWithInstanceVariableFromVariable.py')

        result, _ = await self.call('get_val1', [], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('get_val2', [], return_type=int)
        self.assertEqual(2, result)

    async def test_user_class_update_instance_variable(self):
        await self.set_up_contract('UserClassUpdateInstanceVariable.py')
        from boa3_test.test_sc.class_test.UserClassUpdateInstanceVariable import Example

        expected_result = Example()
        expected_result.val1 = 10
        result, _ = await self.call('get_val', [10], return_type=list)
        self.assertObjectEqual(expected_result, result)

        expected_result.val1 = 40
        result, _ = await self.call('get_val', [40], return_type=list)
        self.assertObjectEqual(expected_result, result)

    async def test_user_class_access_variable_on_init(self):
        await self.set_up_contract('UserClassAccessInstanceVariableOnInit.py')
        from boa3_test.test_sc.class_test.UserClassAccessInstanceVariableOnInit import Example

        result, _ = await self.call('get_obj', [], return_type=list)
        self.assertObjectEqual(Example(), result)

    async def test_user_class_access_variable_on_method(self):
        await self.set_up_contract('UserClassAccessInstanceVariableOnMethod.py')

        result, _ = await self.call('get_val1', [], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('get_val2', [], return_type=int)
        self.assertEqual(4, result)

    def test_user_class_with_base(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'UserClassWithBuiltinBase.py')

    async def test_user_class_with_created_base(self):
        await self.set_up_contract('UserClassWithCreatedBase.py')

        result, _ = await self.call('implemented_method', [], return_type=int)
        self.assertEqual(42, result)

        result, _ = await self.call('inherited_method', [], return_type=int)
        self.assertEqual(42, result)

    async def test_user_class_with_cascated_created_base(self):
        await self.set_up_contract('UserClassWithCascadeCreatedBase.py')

        result, _ = await self.call('implemented_method', [], return_type=int)
        self.assertEqual(42, result)

        result, _ = await self.call('inherited_method', [], return_type=int)
        self.assertEqual(42, result)

    async def test_user_class_with_created_base_with_variable(self):
        await self.set_up_contract('UserClassWithCreatedBaseWithVariables.py')

        result, _ = await self.call('implemented_variable', [], return_type=int)
        self.assertEqual(42, result)

        result, _ = await self.call('inherited_variable', [], return_type=int)
        self.assertEqual(42, result)

        new_value = 10
        result, _ = await self.call('update_variable', [new_value], return_type=int)
        self.assertEqual(new_value, result)

        new_value = -10
        result, _ = await self.call('update_variable', [new_value], return_type=int)
        self.assertEqual(new_value, result)

        new_value = 10_000_000
        result, _ = await self.call('update_variable', [new_value], return_type=int)
        self.assertEqual(new_value, result)

    async def test_user_class_with_created_base_with_args(self):
        await self.set_up_contract('UserClassWithCreatedBaseWithArgs.py')

        init_value = 42
        result, _ = await self.call('implemented_var', [init_value], return_type=int)
        self.assertEqual(init_value, result)

        result, _ = await self.call('inherited_var', [init_value], return_type=int)
        self.assertEqual(init_value, result)

        init_value = -42
        result, _ = await self.call('implemented_var', [init_value], return_type=int)
        self.assertEqual(init_value, result)

        result, _ = await self.call('inherited_var', [init_value], return_type=int)
        self.assertEqual(init_value, result)

        init_value = 10_000_000
        result, _ = await self.call('implemented_var', [init_value], return_type=int)
        self.assertEqual(init_value, result)

        result, _ = await self.call('inherited_var', [init_value], return_type=int)
        self.assertEqual(init_value, result)

    async def test_user_class_with_created_base_with_init(self):
        await self.set_up_contract('UserClassWithCreatedBaseWithInit.py')

        expected_result = 42
        result, _ = await self.call('inherited_var', [], return_type=int)
        self.assertEqual(expected_result, result)

    async def test_user_class_with_created_base_with_init_with_args(self):
        await self.set_up_contract('UserClassWithCreatedBaseWithInitWithArgs.py')

        expected_result = -10
        result, _ = await self.call('inherited_var', [], return_type=int)
        self.assertEqual(expected_result, result)

    async def test_user_class_with_created_base_with_more_variables(self):
        await self.set_up_contract('UserClassWithCreatedBaseWithMoreVariables.py')
        from boa3_test.test_sc.class_test.UserClassWithCreatedBaseWithMoreVariables import Example

        expected_result = Example()
        result, _ = await self.call('get_full_object', [], return_type=list)
        self.assertObjectEqual(expected_result, result)

    def test_user_class_with_created_base_with_more_variables_without_super_init(self):
        self.assertCompilerLogs(CompilerError.MissingInitCall, 'UserClassWithCreatedBaseWithMoreVariablesWithoutSuperInit.py')

    def test_user_class_with_multiple_bases(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'UserClassWithMultipleBases.py')

    def test_user_class_with_keyword_base(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'UserClassWithKeywordBase.py')

    def test_user_class_with_decorator(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'UserClassWithDecorator.py')

    async def test_user_class_with_property_from_object(self):
        await self.set_up_contract('UserClassWithPropertyFromObject.py')

        result, _ = await self.call('get_property', [], return_type=int)
        self.assertEqual(1, result)

    async def test_user_class_with_property_using_instance_variables_from_object(self):
        await self.set_up_contract('UserClassWithPropertyUsingInstanceVariablesFromObject.py')

        result, _ = await self.call('get_property', [], return_type=int)
        self.assertEqual(10, result)

    async def test_user_class_with_property_using_class_variables_from_object(self):
        await self.set_up_contract('UserClassWithPropertyUsingClassVariablesFromObject.py')

        result, _ = await self.call('get_property', [], return_type=int)
        self.assertEqual(10, result)

    async def test_user_class_with_property_using_variables_from_object(self):
        await self.set_up_contract('UserClassWithPropertyUsingVariablesFromObject.py')

        result, _ = await self.call('get_property', [], return_type=int)
        self.assertEqual(47, result)

    def test_user_class_with_property_from_class(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'UserClassWithPropertyFromClass.py')

    def test_user_class_with_property_using_arguments(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'UserClassWithPropertyUsingArguments.py')

    def test_user_class_with_property_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'UserClassWithPropertyMismatchedType.py')

    def test_user_class_with_property_without_self(self):
        self.assertCompilerLogs(CompilerError.SelfArgumentError, 'UserClassWithPropertyWithoutSelf.py')

    async def test_user_class_with_augmented_assignment_operator_with_variable(self):
        await self.set_up_contract('UserClassWithAugmentedAssignmentOperatorWithVariable.py')

        result, _ = await self.call('add', [], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('sub', [], return_type=int)
        self.assertEqual(-2, result)

        result, _ = await self.call('mult', [], return_type=int)
        self.assertEqual(16, result)

        result, _ = await self.call('div', [], return_type=int)
        self.assertEqual(2, result)

        result, _ = await self.call('mod', [], return_type=int)
        self.assertEqual(1, result)

        result, _ = await self.call('mix', [], return_type=int)
        self.assertEqual(0, result)

    async def test_user_class_with_deploy_method(self):
        await self.set_up_contract('UserClassWithDeployMethod.py')
        from boa3_test.test_sc.class_test.UserClassWithDeployMethod import Example

        result, _ = await self.call('get_obj', [], return_type=list)
        self.assertObjectEqual(Example(), result)

    def test_del_class(self):
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, 'DelClass.py')

    async def test_class_property_and_parameter_with_same_name(self):
        await self.set_up_contract('ClassPropertyAndParameterWithSameName.py')

        result, _ = await self.call('main', ['unit test'], return_type=str)
        self.assertEqual('unit test', result)

    async def test_return_dict_with_class_attributes(self):
        await self.set_up_contract('ReturnDictWithClassAttributes.py')

        expected_result = {
            'shape': 'Rectangle',
            'color': 'Blue',
            'background': 'Black',
            'size': 'Small'
        }
        result, _ = await self.call('test_only_values', [], return_type=dict[str,str])
        self.assertEqual(expected_result, result)

        expected_result = {
            'Rectangle': 'shape',
            'Blue': 'color',
            'Black': 'background',
            'Small': 'size'
        }
        result, _ = await self.call('test_only_keys', [], return_type=dict[str,str])
        self.assertEqual(expected_result, result)

        expected_result = {
            'Rectangle': 'Rectangle',
            'Blue': 'Blue',
            'Black': 'Black',
            'Small': 'Small'
        }
        result, _ = await self.call('test_pair', [], return_type=dict[str,str])
        self.assertEqual(expected_result, result)
