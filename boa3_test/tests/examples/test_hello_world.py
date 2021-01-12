from boa3.boa3 import Boa3
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestTemplate(BoaTest):

    def test_hello_world_compile(self):
        path = '%s/boa3_test/examples/HelloWorld.py' % self.dirname
        Boa3.compile(path)

    def test_hello_world_main(self):
        path = '%s/boa3_test/examples/HelloWorld.py' % self.dirname
        engine = TestEngine(self.dirname)
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertIsVoid(result)

        self.assertTrue(b'hello' in engine.storage)
        self.assertEqual(b'world', engine.storage[b'hello'])
