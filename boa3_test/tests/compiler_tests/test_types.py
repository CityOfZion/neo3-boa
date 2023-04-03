import ast

from boa3_test.tests.boa_test import BoaTest  # needs to be the first import to avoid circular imports

from boa3.internal.analyser.analyser import Analyser
from boa3.internal.analyser.typeanalyser import TypeAnalyser
from boa3.internal.model.type.annotation.uniontype import UnionType
from boa3.internal.model.type.collection.sequence.mutable.listtype import ListType
from boa3.internal.model.type.collection.sequence.tupletype import TupleType
from boa3.internal.model.type.type import Type


class TestTypes(BoaTest):

    def test_small_integer_constant(self):
        input = 42
        node = ast.parse(str(input)).body[0].value
        expected_output = Type.int

        typeanalyser = TypeAnalyser(Analyser(node), {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_negative_integer_constant(self):
        input = -10
        node = ast.parse(str(input)).body[0].value
        expected_output = Type.int

        typeanalyser = TypeAnalyser(Analyser(node), {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_boolean_constant(self):
        input = True
        node = ast.parse(str(input)).body[0].value
        expected_output = Type.bool

        typeanalyser = TypeAnalyser(Analyser(node), {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_string_constant(self):
        input = 'unit_test'
        node = ast.parse(str(input)).body[0].value
        expected_output = Type.str

        typeanalyser = TypeAnalyser(Analyser(node), {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_integer_tuple_constant(self):
        input = (1, 2, 3)
        node = ast.parse(str(input)).body[0].value
        expected_output = TupleType(Type.int)

        typeanalyser = TypeAnalyser(Analyser(node), {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_boolean_tuple_constant(self):
        input = (True, False)
        node = ast.parse(str(input)).body[0].value
        expected_output = TupleType(Type.bool)

        typeanalyser = TypeAnalyser(Analyser(node), {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_string_tuple_constant(self):
        input = (1, 2, 3)
        node = ast.parse(str(input)).body[0].value
        expected_output = TupleType(Type.int)

        typeanalyser = TypeAnalyser(Analyser(node), {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_any_tuple_constant(self):
        input = (1, '2', False)
        node = ast.parse(str(input)).body[0].value
        expected_output = TupleType(UnionType.build([Type.str,
                                                     Type.int]))

        typeanalyser = TypeAnalyser(Analyser(node), {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_integer_list_constant(self):
        input = [1, 2, 3]
        node = ast.parse(str(input)).body[0].value
        expected_output = ListType(Type.int)

        typeanalyser = TypeAnalyser(Analyser(node), {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_boolean_list_constant(self):
        input = [True, False]
        node = ast.parse(str(input)).body[0].value
        expected_output = ListType(Type.bool)

        typeanalyser = TypeAnalyser(Analyser(node), {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_string_list_constant(self):
        input = [1, 2, 3]
        node = ast.parse(str(input)).body[0].value
        expected_output = ListType(Type.int)

        typeanalyser = TypeAnalyser(Analyser(node), {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_any_list_constant(self):
        input = [1, '2', False]
        node = ast.parse(str(input)).body[0].value
        expected_output = ListType(UnionType.build([Type.int,
                                                    Type.str]))

        typeanalyser = TypeAnalyser(Analyser(node), {})
        output = typeanalyser.get_type(input)

        self.assertEqual(expected_output, output)

    def test_sequence_any_is_type_of_str(self):
        sequence_type = Type.sequence
        str_type = Type.str
        self.assertTrue(sequence_type.is_type_of(str_type))

    def test_sequence_any_is_type_of_tuple_any(self):
        sequence_type = Type.sequence
        tuple_type = Type.tuple
        self.assertTrue(sequence_type.is_type_of(tuple_type))

    def test_sequence_int_is_type_of_tuple_any(self):
        sequence_type = Type.sequence.build_collection(Type.int)
        tuple_type = Type.tuple
        self.assertFalse(sequence_type.is_type_of(tuple_type))

    def test_sequence_any_is_type_of_tuple_int(self):
        sequence_type = Type.sequence
        tuple_type = Type.tuple.build_collection(Type.int)
        self.assertTrue(sequence_type.is_type_of(tuple_type))

    def test_sequence_any_is_type_of_list_any(self):
        sequence_type = Type.sequence
        list_type = Type.list
        self.assertTrue(sequence_type.is_type_of(list_type))

    def test_sequence_int_is_type_of_list_any(self):
        sequence_type = Type.sequence.build_collection(Type.int)
        list_type = Type.list
        self.assertFalse(sequence_type.is_type_of(list_type))

    def test_sequence_any_is_type_of_list_int(self):
        sequence_type = Type.sequence
        list_type = Type.list.build_collection(Type.int)
        self.assertTrue(sequence_type.is_type_of(list_type))

    def test_tuple_any_is_type_of_sequence(self):
        sequence_type = Type.sequence
        tuple_type = Type.tuple
        self.assertFalse(tuple_type.is_type_of(sequence_type))

    def test_tuple_any_is_type_of_tuple_int(self):
        tuple_type = Type.tuple
        tuple_int_type = Type.tuple.build_collection(Type.int)
        self.assertTrue(tuple_type.is_type_of(tuple_int_type))

    def test_tuple_int_is_type_of_tuple_any(self):
        tuple_type = Type.tuple.build_collection(Type.int)
        tuple_any_type = Type.tuple
        self.assertFalse(tuple_type.is_type_of(tuple_any_type))

    def test_list_any_is_type_of_sequence(self):
        list_type = Type.list
        sequence_type = Type.sequence
        self.assertFalse(list_type.is_type_of(sequence_type))

    def test_list_any_is_type_of_list_int(self):
        list_type = Type.list
        list_int_type = Type.list.build_collection(Type.int)
        self.assertTrue(list_type.is_type_of(list_int_type))

    def test_list_int_is_type_of_list_any(self):
        list_type = Type.list.build_collection(Type.int)
        list_any_type = Type.list
        self.assertFalse(list_type.is_type_of(list_any_type))

    def test_str_any_is_type_of_sequence(self):
        sequence_type = Type.sequence
        str_type = Type.str
        self.assertFalse(str_type.is_type_of(sequence_type))

    def test_str_any_is_type_of_sequence_str(self):
        sequence_type = Type.sequence.build_collection(Type.str)
        str_type = Type.str
        self.assertFalse(str_type.is_type_of(sequence_type))

    def test_optional_is_type_of_union(self):
        optional_type = Type.optional.build(Type.str)
        union_type = Type.union.build({Type.str, Type.none})
        self.assertTrue(optional_type.is_type_of(union_type))
        self.assertTrue(union_type.is_type_of(optional_type))

        optional_type = Type.optional.build({Type.str, Type.int, Type.bool, Type.bytes})
        union_type = Type.union.build({Type.str, Type.int, Type.bool, Type.bytes, Type.none})
        self.assertTrue(optional_type.is_type_of(union_type))
        self.assertTrue(union_type.is_type_of(optional_type))

        optional_type = Type.optional.build(Type.str)
        union_type = Type.union.build({Type.str, Type.int, Type.bool, Type.bytes, Type.none})
        self.assertFalse(optional_type.is_type_of(union_type))
        self.assertTrue(union_type.is_type_of(optional_type))

        optional_type = Type.optional.build({Type.str, Type.int, Type.bool, Type.bytes})
        union_type = Type.union.build({Type.str})
        self.assertTrue(optional_type.is_type_of(union_type))
        self.assertFalse(union_type.is_type_of(optional_type))

        optional_type = Type.optional.build({Type.str, Type.int, Type.bool, Type.bytes})
        union_type = Type.union.build({Type.str, Type.int, Type.bool, Type.bytes})
        self.assertTrue(optional_type.is_type_of(union_type))
        self.assertFalse(union_type.is_type_of(optional_type))

        optional_type = Type.optional.build(Type.any)
        union_type = Type.union.build({Type.str, Type.int, Type.bool, Type.bytes, Type.none})
        self.assertTrue(optional_type.is_type_of(union_type))
        self.assertFalse(union_type.is_type_of(optional_type))

        optional_type = Type.optional.build({Type.str, Type.int, Type.bool, Type.bytes, Type.none})
        union_type = Type.union.build(Type.any)
        self.assertFalse(optional_type.is_type_of(union_type))
        self.assertTrue(union_type.is_type_of(optional_type))
