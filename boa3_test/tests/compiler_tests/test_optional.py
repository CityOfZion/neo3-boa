from boa3.boa3 import Boa3
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.testengine import TestEngine


class TestOptional(BoaTest):

    default_folder: str = 'test_sc/optional_test'

    def test_optional_return(self):
        path = self.get_contract_path('OptionalReturn.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 1)
        self.assertEqual('str', result)
        result = self.run_smart_contract(engine, path, 'main', 2)
        self.assertEqual(123, result)
        result = self.run_smart_contract(engine, path, 'main', 3)
        self.assertEqual(None, result)

        result = self.run_smart_contract(engine, path, 'union_test', 1)
        self.assertEqual('str', result)
        result = self.run_smart_contract(engine, path, 'union_test', 2)
        self.assertEqual(123, result)
        result = self.run_smart_contract(engine, path, 'union_test', 3)
        self.assertEqual(None, result)

    def test_optional_variable_reassign(self):
        expected_output = (
            Opcode.INITSLOT  # function signature
            + b'\x03'
            + b'\x00'
            + Opcode.PUSH2  # a = 2
            + Opcode.STLOC0
            + Opcode.PUSH2  # b = a
            + Opcode.STLOC1
            + Opcode.PUSHNULL  # c = None
            + Opcode.STLOC2
            + Opcode.LDLOC2  # b = c
            + Opcode.STLOC1
            + Opcode.RET  # return
        )

        path = self.get_contract_path('OptionalVariableReassign.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

    def test_optional_variable_argument(self):
        path = self.get_contract_path('OptionalVariableArgument.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 'unittest')
        self.assertEqual('string', result)
        result = self.run_smart_contract(engine, path, 'main', 123)
        self.assertEqual('int', result)
        result = self.run_smart_contract(engine, path, 'main', None)
        self.assertEqual('None', result)

        result = self.run_smart_contract(engine, path, 'union_test', 'unittest')
        self.assertEqual('string', result)
        result = self.run_smart_contract(engine, path, 'union_test', 123)
        self.assertEqual('int', result)
        result = self.run_smart_contract(engine, path, 'union_test', None)
        self.assertEqual('None', result)

    def test_optional_isinstance_validation(self):
        path = self.get_contract_path('OptionalIsInstanceValidation.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main', 'unittest')
        self.assertEqual('unittest', result)
        result = self.run_smart_contract(engine, path, 'main', 123)
        self.assertEqual('int', result)
        result = self.run_smart_contract(engine, path, 'main', None)
        self.assertEqual('None', result)

        result = self.run_smart_contract(engine, path, 'union_test', 'unittest')
        self.assertEqual('unittest', result)
        result = self.run_smart_contract(engine, path, 'union_test', 123)
        self.assertEqual('int', result)
        result = self.run_smart_contract(engine, path, 'union_test', None)
        self.assertEqual('None', result)
