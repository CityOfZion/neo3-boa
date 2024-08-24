from boa3.internal.exception import CompilerError
from boa3_test.tests import boatestcase


class TestMatchCase(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/match_case_test'

    async def test_any_type_match_case(self):
        await self.set_up_contract('AnyTypeMatchCase.py')

        def match_case(x) -> str:
            match x:
                case True:
                    return "True"
                case 1:
                    return "one"
                case "2":
                    return "2 string"
                case {}:
                    return "dictionary"
                case _:
                    # this is the default case, when all others are False
                    return "other"

        arg = True
        result, _ = await self.call('main', [arg], return_type=str)
        self.assertEqual(match_case(arg), result)

        arg = 1
        result, _ = await self.call('main', [arg], return_type=str)
        self.assertEqual(match_case(arg), result)

        arg = "2"
        result, _ = await self.call('main', [arg], return_type=str)
        self.assertEqual(match_case(arg), result)

        arg = {'any': 'dict'}
        result, _ = await self.call('main', [arg], return_type=str)
        self.assertEqual(match_case(arg), result)

        arg = 'other value'
        result, _ = await self.call('main', [arg], return_type=str)
        self.assertEqual(match_case(arg), result)

    async def test_bool_type_match_case(self):
        await self.set_up_contract('BoolTypeMatchCase.py')

        result, _ = await self.call('main', [True], return_type=str)
        self.assertEqual("True", result)

        result, _ = await self.call('main', [False], return_type=str)
        self.assertEqual("False", result)

    async def test_int_type_match_case(self):
        await self.set_up_contract('IntTypeMatchCase.py')

        result, _ = await self.call('main', [10], return_type=str)
        self.assertEqual("ten", result)

        result, _ = await self.call('main', [-10], return_type=str)
        self.assertEqual("minus ten", result)

        result, _ = await self.call('main', [0], return_type=str)
        self.assertEqual("zero", result)

        result, _ = await self.call('main', [123], return_type=str)
        self.assertEqual("other", result)
        result, _ = await self.call('main', [-999], return_type=str)
        self.assertEqual("other", result)

    async def test_str_type_match_case(self):
        await self.set_up_contract('StrTypeMatchCase.py')

        result, _ = await self.call('main', ['first'], return_type=str)
        self.assertEqual("1", result)

        result, _ = await self.call('main', ['second'], return_type=str)
        self.assertEqual("2", result)

        result, _ = await self.call('main', ['third'], return_type=str)
        self.assertEqual("3", result)

        result, _ = await self.call('main', ['another value'], return_type=str)
        self.assertEqual("other", result)

        result, _ = await self.call('main', ['unit test'], return_type=str)
        self.assertEqual("other", result)

    async def test_dict_type_match_case(self):
        await self.set_up_contract('DictTypeMatchCase.py')

        def match_case(dict_: dict) -> str:
            match dict_:
                case {
                    'ccccc': None,
                    'ab': 'cd',
                    '12': '34',
                    'xy': 'zy',
                    '00': '55',
                }:
                    return "big dictionary"
                case {'key': 'value'}:
                    return "key and value"
                case {}:
                    return "empty dict"
                case _:
                    return "default return"

        arg = {}
        result, _ = await self.call('main', [arg], return_type=str)
        self.assertEqual(match_case(arg), result)

        arg = {'key': 'value'}
        result, _ = await self.call('main', [arg], return_type=str)
        self.assertEqual(match_case(arg), result)

        arg = {'key': 'value', 'unit': 'test'}
        result, _ = await self.call('main', [arg], return_type=str)
        self.assertEqual(match_case(arg), result)

        arg = {'another': 'pair'}
        result, _ = await self.call('main', [arg], return_type=str)
        self.assertEqual(match_case(arg), result)

        arg = {
            'ccccc': None,
            'ab': 'cd',
            '12': '34',
            'xy': 'zy',
            '00': '55',
        }
        result, _ = await self.call('main', [arg], return_type=str)
        self.assertEqual(match_case(arg), result)

    async def test_outer_var_inside_match(self):
        await self.set_up_contract('OuterVariableInsideMatch.py')

        result, _ = await self.call('main', [True], return_type=str)
        self.assertEqual("String is: True", result)

        result, _ = await self.call('main', [10], return_type=str)
        self.assertEqual("String is: 10", result)

        result, _ = await self.call('main', ["2"], return_type=str)
        self.assertEqual("String is: 2 string", result)

        result, _ = await self.call('main', ['another value'], return_type=str)
        self.assertEqual("String is: other", result)

        result, _ = await self.call('main', ['unit test'], return_type=str)
        self.assertEqual("String is: other", result)

    async def test_var_existing_in_all_cases(self):
        await self.set_up_contract('VarExistingInAllCases.py')

        result, _ = await self.call('main', [True], return_type=str)
        self.assertEqual("True", result)

        result, _ = await self.call('main', [10], return_type=str)
        self.assertEqual("10", result)

        result, _ = await self.call('main', ["2"], return_type=str)
        self.assertEqual("2 string", result)

        result, _ = await self.call('main', ['another value'], return_type=str)
        self.assertEqual("other", result)

        result, _ = await self.call('main', ['unit test'], return_type=str)
        self.assertEqual("other", result)

    def test_unsupported_case(self):
        path = self.get_contract_path('UnsupportedCase.py')
        self.assertCompilerLogs(CompilerError.NotSupportedOperation, path)
