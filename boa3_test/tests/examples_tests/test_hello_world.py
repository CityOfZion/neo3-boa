from boa3_test.tests import boatestcase


class TestTemplate(boatestcase.BoaTestCase):
    default_folder: str = 'examples'

    def test_hello_world_compile(self):
        path = self.get_contract_path('hello_world.py')
        self.assertCompile(path)

    async def test_hello_world_main(self):
        await self.set_up_contract('hello_world.py')

        result, _ = await self.call('Main', [], return_type=None, signing_accounts=[self.genesis])
        self.assertIsNone(result)

        key = b'hello'
        expected_value = b'world'

        contract_storage = await self.get_storage()
        self.assertIn(key, contract_storage)
        self.assertEqual(expected_value, contract_storage[key])
