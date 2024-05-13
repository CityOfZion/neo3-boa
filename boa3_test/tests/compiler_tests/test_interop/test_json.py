import json

from boa3_test.tests import boatestcase
from boa3.internal.exception import CompilerWarning


class TestJsonInterop(boatestcase.BoaTestCase):
    default_folder: str = 'test_sc/interop_test/json'

    async def test_json_serialize(self):
        await self.set_up_contract('JsonSerialize.py')

        test_input = {"one": 1, "two": 2, "three": 3}
        expected_result = json.dumps(test_input, separators=(',', ':'))
        result, _ = await self.call('main', [test_input], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_json_serialize_int(self):
        await self.set_up_contract('JsonSerializeInt.py')

        expected_result = json.dumps(10)
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_json_serialize_bool(self):
        await self.set_up_contract('JsonSerializeBool.py')

        expected_result = json.dumps(True)
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_json_serialize_str(self):
        await self.set_up_contract('JsonSerializeStr.py')

        expected_result = json.dumps('unit test')
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_json_serialize_bytes(self):
        await self.set_up_contract('JsonSerializeBytes.py')

        # Python does not accept bytes as parameter for json.dumps() method, since string and bytes ends up being the
        # same on Neo, it's being converted to string, before using dumps
        expected_result = json.dumps('unit test')
        result, _ = await self.call('main', [], return_type=str)
        self.assertEqual(expected_result, result)

    async def test_json_deserialize(self):
        await self.set_up_contract('JsonDeserialize.py')

        test_input = json.dumps(12345)
        expected_result = json.loads(test_input)
        result, _ = await self.call('main', [test_input], return_type=int)
        self.assertEqual(expected_result, result)

        test_input = json.dumps('unit test')
        expected_result = json.loads(test_input)
        result, _ = await self.call('main', [test_input], return_type=str)
        self.assertEqual(expected_result, result)

        test_input = json.dumps(True)
        expected_result = json.loads(test_input)
        result, _ = await self.call('main', [test_input], return_type=bool)
        self.assertEqual(expected_result, result)

    async def test_import_json(self):
        self.assertCompilerLogs(CompilerWarning.DeprecatedSymbol, 'ImportJson.py')
        await self.set_up_contract('ImportJson.py')

        value = 123
        result, _ = await self.call('main', [value], return_type=int)
        self.assertEqual(value, result)

        value = 'string'
        result, _ = await self.call('main', [value], return_type=str)

    async def test_import_interop_json(self):
        self.assertCompilerLogs(CompilerWarning.DeprecatedSymbol, 'ImportInteropJson.py')
        await self.set_up_contract('ImportInteropJson.py')

        value = 123
        result, _ = await self.call('main', [value], return_type=int)
        self.assertEqual(value, result)

        value = 'string'
        result, _ = await self.call('main', [value], return_type=str)
        self.assertEqual(value, result)
