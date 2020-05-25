import ast

from boa3.analyser.typeanalyser import TypeAnalyser
from boa3.model.type.tupletype import TupleType
from boa3.model.type.type import Type
from boa3_test.tests.boa_test import BoaTest


class TestTypes(BoaTest):

    def test_small_integer_constant(self):
        input = 42
        node = ast.parse(str(input)).body[0].value
        expected_output = Type.int

        typeanalyser = TypeAnalyser(node, {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_negative_integer_constant(self):
        input = -10
        node = ast.parse(str(input)).body[0].value
        expected_output = Type.int

        typeanalyser = TypeAnalyser(node, {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_boolean_constant(self):
        input = True
        node = ast.parse(str(input)).body[0].value
        expected_output = Type.bool

        typeanalyser = TypeAnalyser(node, {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_string_constant(self):
        input = 'unit_test'
        node = ast.parse(str(input)).body[0].value
        expected_output = Type.str

        typeanalyser = TypeAnalyser(node, {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_integer_tuple_constant(self):
        input = (1, 2, 3)
        node = ast.parse(str(input)).body[0].value
        expected_output = TupleType(Type.int)

        typeanalyser = TypeAnalyser(node, {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_boolean_tuple_constant(self):
        input = (True, False)
        node = ast.parse(str(input)).body[0].value
        expected_output = TupleType(Type.bool)

        typeanalyser = TypeAnalyser(node, {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_string_tuple_constant(self):
        input = (1, 2, 3)
        node = ast.parse(str(input)).body[0].value
        expected_output = TupleType(Type.int)

        typeanalyser = TypeAnalyser(node, {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_any_tuple_constant(self):
        input = (1, '2', False)
        node = ast.parse(str(input)).body[0].value
        expected_output = TupleType(Type.none)  # TODO: change to any when implemented

        typeanalyser = TypeAnalyser(node, {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)
