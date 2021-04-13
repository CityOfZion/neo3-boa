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
        self.assertEqual(len(engine.notifications), 0)
        self.assertEqual(bytes(20), result)

        result = self.run_smart_contract(engine, path, 'event_name', [])
        self.assertEqual(len(engine.notifications), 0)
        self.assertEqual('', result)

        result = self.run_smart_contract(engine, path, 'state', [])
        self.assertEqual(len(engine.notifications), 0)
        self.assertEqual([], result)

        result = self.run_smart_contract(engine, path, 'script_hash', [1])
        self.assertEqual(len(engine.notifications), 1)
        self.assertEqual(script, result)

        engine.reset_engine()
        result = self.run_smart_contract(engine, path, 'event_name', [1])
        self.assertEqual(len(engine.notifications), 1)
        self.assertEqual('notify', result)

        engine.reset_engine()
        result = self.run_smart_contract(engine, path, 'state', [1])
        self.assertEqual(len(engine.notifications), 1)
        self.assertEqual([1], result)

        engine.reset_engine()
        result = self.run_smart_contract(engine, path, 'state', ['1'])
        self.assertEqual(len(engine.notifications), 1)
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
        output, manifest = self.compile_and_save(path)

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
