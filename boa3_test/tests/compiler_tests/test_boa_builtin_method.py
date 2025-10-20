from boa3.internal import constants
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.StackItem import StackItemType
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestBoaBuiltinMethod(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/boa_built_in_methods_test'

    async def test_abort(self):
        await self.set_up_contract('Abort.py')

        result, _ = await self.call('main', [False], return_type=int)
        self.assertEqual(123, result)

        with self.assertRaises(boatestcase.AbortException) as context:
            await self.call('main', [True], return_type=int)

        self.assertIsNone(context.exception.args[0])

    def test_abort_with_message_compile(self):
        assert_msg = String('abort was called').to_bytes()
        number_123 = Integer(123).to_byte_array(signed=True, min_length=1)

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x01'
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if check:
            + Opcode.PUSH5
            + Opcode.PUSHDATA1
            + Integer(len(assert_msg)).to_byte_array() + assert_msg
            + Opcode.ABORTMSG   # abort('abort was called')
            + Opcode.PUSHINT8
            + number_123        # return 123
            + Opcode.RET
        )

        output, _ = self.assertCompile('AbortWithMessage.py')
        self.assertEqual(expected_output, output)

    async def test_abort_with_message_run(self):
        await self.set_up_contract('AbortWithMessage.py')

        result, _ = await self.call('main', [False], return_type=int)
        self.assertEqual(123, result)

        with self.assertRaises(boatestcase.AbortException) as context:
            await self.call('main', [True], return_type=int)

        self.assertRegex(str(context.exception), 'abort was called')

    def test_abort_with_optional_message_compile(self):
        number_123 = Integer(123).to_byte_array(signed=True, min_length=1)

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x00'
            + b'\x02'
            + Opcode.LDARG0
            + Opcode.JMPIFNOT   # if check:
            + Integer(11).to_byte_array(signed=True, min_length=1)
            + Opcode.LDARG1
            + Opcode.DUP
            + Opcode.ISTYPE + StackItemType.ByteString
            + Opcode.JMPIF
            + Integer(3).to_byte_array(signed=True, min_length=1)
            + Opcode.ABORT
            + Opcode.ABORTMSG   # abort('abort was called')
            + Opcode.DROP
            + Opcode.PUSHINT8
            + number_123        # return 123
            + Opcode.RET
        )

        output, _ = self.assertCompile('AbortWithOptionalMessage.py')
        self.assertEqual(expected_output, output)

    async def test_abort_with_optional_message_run(self):
        await self.set_up_contract('AbortWithOptionalMessage.py')

        result, _ = await self.call('main', [False, None], return_type=int)
        self.assertEqual(123, result)

        with self.assertRaises(boatestcase.AbortException) as context:
            await self.call('main', [True, None], return_type=int)

        self.assertIsNone(context.exception.args[0])

        abort_message = 'Off chain message'
        with self.assertRaises(boatestcase.AbortException) as context:
            await self.call('main', [True, abort_message], return_type=int)

        self.assertRegex(str(context.exception), abort_message)

    async def test_env(self):
        test_smart_contract_name = 'Env.py'
        custom_env = 'testnet'
        custom_name = f'Env_{custom_env}.nef'

        await self.set_up_contract(test_smart_contract_name)
        custom_env_contract = await self.compile_and_deploy(test_smart_contract_name,
                                                            env=custom_env,
                                                            output_name=custom_name,
                                                            change_manifest_name=True
                                                            )

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(constants.DEFAULT_CONTRACT_ENVIRONMENT, result)

        result, _ = await self.call('main', [], return_type=str,
                                    target_contract=custom_env_contract)
        self.assertEqual(custom_env, result)

    # region _deploy

    async def test_deploy_def(self):
        await self.set_up_contract('DeployDef.py')

        result, _ = await self.call('get_var', [], return_type=int)
        self.assertEqual(10, result)

    async def test_deploy_reassign_variable(self):
        await self.set_up_contract('DeployReassignVariable.py')

        result, _ = await self.call('main', [], return_type=int)
        self.assertEqual(123, result)

    def test_deploy_def_incorrect_signature(self):
        self.assertCompilerLogs(CompilerError.InternalIncorrectSignature, 'DeployDefWrongSignature.py')

    async def test_deploy_with_import_var(self):
        await self.set_up_contract('DeployWithImportVar.py')

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual('bar', result)

    async def test_deploy_with_import_function(self):
        await self.set_up_contract('DeployWithImportFunction.py')

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual('bar', result)

    async def test_deploy_with_global_var(self):
        await self.set_up_contract('DeployWithGlobalVar.py')

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual('change', result)

    async def test_deploy_with_shadow_var(self):
        await self.set_up_contract('DeployWithShadowVar.py')

        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual('new variable', result)

        result, _ = await self.call('get_global_var', [], return_type=str)
        self.assertEqual('shadow', result)

    async def test_deploy_with_import_class(self):
        await self.set_up_contract('DeployWithImportClass.py')
        from boa3_test.test_sc.import_test.class_import.example import Example

        result, _ = await self.call('main', [], return_type=list)
        self.assertObjectEqual(Example(42, '42'), result)

    # endregion

    def test_will_not_compile(self):
        self.assertCompilerLogs(CompilerError.UnresolvedReference, 'WillNotCompile.py')

    # region math builtins

    async def test_sqrt_method(self):
        await self.set_up_contract('Sqrt.py')

        from math import sqrt

        expected_result = int(sqrt(0))
        result, _ = await self.call('main', [0], return_type=int)
        self.assertEqual(expected_result, result)

        expected_result = int(sqrt(1))
        result, _ = await self.call('main', [1], return_type=int)
        self.assertEqual(expected_result, result)

        expected_result = int(sqrt(3))
        result, _ = await self.call('main', [3], return_type=int)
        self.assertEqual(expected_result, result)

        expected_result = int(sqrt(4))
        result, _ = await self.call('main', [4], return_type=int)
        self.assertEqual(expected_result, result)

        expected_result = int(sqrt(8))
        result, _ = await self.call('main', [8], return_type=int)
        self.assertEqual(expected_result, result)

        expected_result = int(sqrt(10))
        result, _ = await self.call('main', [10], return_type=int)
        self.assertEqual(expected_result, result)

        val = 25
        expected_result = int(sqrt(val))
        result, _ = await self.call('main', [val], return_type=int)
        self.assertEqual(expected_result, result)

        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [-1], return_type=int)

        self.assertRegex(str(context.exception), 'negative value')

    async def test_sqrt_method_from_math(self):
        await self.set_up_contract('SqrtFromMath.py')

        from math import sqrt

        val = 25
        expected_result = int(sqrt(val))
        result, _ = await self.call('main', [val], return_type=int)
        self.assertEqual(expected_result, result)

    async def test_decimal_floor_method(self):
        await self.set_up_contract('DecimalFloor.py')

        from math import floor

        value = 4.2
        decimals = 8

        multiplier = 10 ** decimals
        value_floor = int(floor(value)) * multiplier
        integer_value = int(value * multiplier)
        result, _ = await self.call('main', [integer_value, decimals], return_type=int)
        self.assertEqual(value_floor, result)

        decimals = 12

        multiplier = 10 ** decimals
        value_floor = int(floor(value)) * multiplier
        integer_value = int(value * multiplier)
        result, _ = await self.call('main', [integer_value, decimals], return_type=int)
        self.assertEqual(value_floor, result)

        value = -3.983541

        multiplier = 10 ** decimals
        value_floor = int(floor(value) * multiplier)
        integer_value = int(value * multiplier)
        result, _ = await self.call('main', [integer_value, decimals], return_type=int)
        self.assertEqual(value_floor, result)

        # negative decimals will raise an exception
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [integer_value, -1], return_type=int)

        from boa3.internal.model.builtin.builtin import Builtin
        self.assertRegex(str(context.exception), Builtin.BuiltinMathFloor.exception_message)

    async def test_decimal_ceil_method(self):
        await self.set_up_contract('DecimalCeiling.py')

        from math import ceil

        value = 4.2
        decimals = 8

        multiplier = 10 ** decimals
        value_ceiling = int(ceil(value)) * multiplier
        integer_value = int(value * multiplier)
        result, _ = await self.call('main', [integer_value, decimals], return_type=int)
        self.assertEqual(value_ceiling, result)

        decimals = 12

        multiplier = 10 ** decimals
        value_ceiling = int(ceil(value)) * multiplier
        integer_value = int(value * multiplier)
        result, _ = await self.call('main', [integer_value, decimals], return_type=int)
        self.assertEqual(value_ceiling, result)

        value = -3.983541

        multiplier = 10 ** decimals
        value_ceiling = int(ceil(value) * multiplier)
        integer_value = int(value * multiplier)
        result, _ = await self.call('main', [integer_value, decimals], return_type=int)
        self.assertEqual(value_ceiling, result)

        # negative decimals will raise an exception
        with self.assertRaises(boatestcase.FaultException) as context:
            await self.call('main', [integer_value, -1], return_type=int)

        from boa3.internal.model.builtin.builtin import Builtin
        self.assertRegex(str(context.exception), Builtin.BuiltinMathCeil.exception_message)

    # endregion
