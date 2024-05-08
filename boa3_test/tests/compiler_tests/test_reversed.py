from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.type.String import String
from boa3_test.tests import boatestcase


class TestReversed(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/reversed_test'

    async def test_reversed_list_bool(self):
        await self.set_up_contract('ReversedListBool.py')

        list_bool = [True, True, False]
        reversed_list = list(reversed(list_bool))

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(reversed_list, result)

    async def test_reversed_list_bytes(self):
        await self.set_up_contract('ReversedListBytes.py')

        list_bytes = [b'1', b'2', b'3']
        reversed_list = [String.from_bytes(element) for element in reversed(list_bytes)]

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(reversed_list, result)

    async def test_reversed_list_int(self):
        await self.set_up_contract('ReversedListInt.py')

        list_int = [1, 2, 3]
        reversed_list = list(reversed(list_int))

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(reversed_list, result)

    async def test_reversed_list_str(self):
        await self.set_up_contract('ReversedListStr.py')

        list_str = ['neo3-boa', 'unit', 'test']
        reversed_list = list(reversed(list_str))

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(reversed_list, result)

    async def test_reversed_list(self):
        await self.set_up_contract('ReversedList.py')

        list_any = [1, 'string', False]
        reversed_list = list(reversed(list_any))

        result, _ = await self.call('main', [list_any], return_type=list)
        self.assertEqual(reversed_list, result)

    async def test_reversed_string(self):
        await self.set_up_contract('ReversedString.py')

        string = 'unit_test'
        reversed_list = list(reversed(string))

        result, _ = await self.call('main', [string], return_type=list)
        self.assertEqual(reversed_list, result)

    async def test_reversed_bytes(self):
        await self.set_up_contract('ReversedBytes.py')

        bytes_value = b'unit_test'
        reversed_list = list(reversed(bytes_value))

        result, _ = await self.call('main', [bytes_value], return_type=list)
        self.assertEqual(reversed_list, result)

    async def test_reversed_range(self):
        await self.set_up_contract('ReversedRange.py')

        reversed_list = list(reversed(range(3)))

        result, _ = await self.call('main', [], return_type=list)
        self.assertEqual(reversed_list, result)

    async def test_reversed_tuple(self):
        await self.set_up_contract('ReversedTuple.py')

        tuple_value = (1, 2, 3)
        reversed_list = list(reversed(tuple_value))

        result, _ = await self.call('main', [tuple_value], return_type=list)
        self.assertEqual(reversed_list, result)

    def test_mismatched_type(self):
        self.assertCompilerLogs(CompilerError.MismatchedTypes, 'ReversedParameterMismatchedType')
