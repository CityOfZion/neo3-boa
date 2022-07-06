from boa3.boa3 import Boa3
from boa3.exception import CompilerError
from boa3.neo.vm.opcode.Opcode import Opcode
from boa3.neo.vm.type.Integer import Integer
from boa3.neo.vm.type.String import String
from boa3_test.tests.boa_test import BoaTest
from boa3_test.tests.test_classes.TestExecutionException import TestExecutionException
from boa3_test.tests.test_classes.testengine import TestEngine


class TestString(BoaTest):
    default_folder: str = 'test_sc/string_test'

    SUBSTRING_NOT_FOUND_MSG = 'substring not found'

    def test_string_get_value(self):
        path = self.get_contract_path('GetValue.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'unit')
        self.assertEqual('u', result)
        result = self.run_smart_contract(engine, path, 'Main', '123')
        self.assertEqual('1', result)

        with self.assertRaisesRegex(TestExecutionException, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX):
            self.run_smart_contract(engine, path, 'Main', '')

    def test_string_get_value_to_variable(self):
        path = self.get_contract_path('GetValueToVariable.py')
        output = Boa3.compile(path)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main', 'unit')
        self.assertEqual('u', result)
        result = self.run_smart_contract(engine, path, 'Main', '123')
        self.assertEqual('1', result)

        with self.assertRaisesRegex(TestExecutionException, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX):
            self.run_smart_contract(engine, path, 'Main', '')

    def test_string_set_value(self):
        path = self.get_contract_path('SetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_string_slicing(self):
        path = self.get_contract_path('StringSlicingLiteralValues.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('i', result)

    def test_string_slicing_start_larger_than_ending(self):
        path = self.get_contract_path('StringSlicingStartLargerThanEnding.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('', result)

    def test_string_slicing_with_variables(self):
        path = self.get_contract_path('StringSlicingVariableValues.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('i', result)

    def test_string_slicing_negative_start(self):
        path = self.get_contract_path('StringSlicingNegativeStart.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'unit_', result)

    def test_string_slicing_negative_end_omitted(self):
        path = self.get_contract_path('StringSlicingNegativeEndOmitted.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('test', result)

    def test_string_slicing_start_omitted(self):
        path = self.get_contract_path('StringSlicingStartOmitted.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'uni', result)

    def test_string_slicing_omitted(self):
        string_value = 'unit_test'
        byte_input = String(string_value).to_bytes()

        expected_output = (
            Opcode.INITSLOT     # function signature
            + b'\x01'
            + b'\x00'
            + Opcode.PUSHDATA1  # a = 'unit_test'
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.STLOC0
            + Opcode.PUSHDATA1  # return a[:3]
            + Integer(len(byte_input)).to_byte_array()
            + byte_input
            + Opcode.RET
        )
        path = self.get_contract_path('StringSlicingOmitted.py')
        output = Boa3.compile(path)
        self.assertEqual(expected_output, output)

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main')
        self.assertEqual('unit_test', result)

    def test_string_slicing_end_omitted(self):
        path = self.get_contract_path('StringSlicingEndOmitted.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'Main',
                                         expected_result_type=bytes)
        self.assertEqual(b'it_test', result)

    def test_string_slicing_with_stride(self):
        path = self.get_contract_path('StringSlicingWithStride.py')
        engine = TestEngine()

        a = 'unit_test'
        expected_result = a[2:5:2]
        result = self.run_smart_contract(engine, path, 'literal_values')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-6:5:2]
        result = self.run_smart_contract(engine, path, 'negative_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[0:-1:2]
        result = self.run_smart_contract(engine, path, 'negative_end')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-6:-1:2]
        result = self.run_smart_contract(engine, path, 'negative_values')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-999:5:2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[0:-999:2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_end')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-999:-999:2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_values')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[999:5:2]
        result = self.run_smart_contract(engine, path, 'really_high_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[0:999:2]
        result = self.run_smart_contract(engine, path, 'really_high_end')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[999:999:2]
        result = self.run_smart_contract(engine, path, 'really_high_values')
        self.assertEqual(expected_result, result)

    def test_string_slicing_with_negative_stride(self):
        path = self.get_contract_path('StringSlicingWithNegativeStride.py')
        engine = TestEngine()

        a = 'unit_test'
        expected_result = a[2:5:-1]
        result = self.run_smart_contract(engine, path, 'literal_values')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-6:5:-1]
        result = self.run_smart_contract(engine, path, 'negative_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[0:-1:-1]
        result = self.run_smart_contract(engine, path, 'negative_end')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-6:-1:-1]
        result = self.run_smart_contract(engine, path, 'negative_values')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-999:5:-1]
        result = self.run_smart_contract(engine, path, 'negative_really_low_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[0:-999:-1]
        result = self.run_smart_contract(engine, path, 'negative_really_low_end')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-999:-999:-1]
        result = self.run_smart_contract(engine, path, 'negative_really_low_values')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[999:5:-1]
        result = self.run_smart_contract(engine, path, 'really_high_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[0:999:-1]
        result = self.run_smart_contract(engine, path, 'really_high_end')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[999:999:-1]
        result = self.run_smart_contract(engine, path, 'really_high_values')
        self.assertEqual(expected_result, result)

    def test_string_slicing_omitted_with_stride(self):
        path = self.get_contract_path('StringSlicingOmittedWithStride.py')
        engine = TestEngine()

        a = 'unit_test'
        expected_result = a[::2]
        result = self.run_smart_contract(engine, path, 'omitted_values')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:5:2]
        result = self.run_smart_contract(engine, path, 'omitted_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[2::2]
        result = self.run_smart_contract(engine, path, 'omitted_end')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-6::2]
        result = self.run_smart_contract(engine, path, 'negative_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:-1:2]
        result = self.run_smart_contract(engine, path, 'negative_end')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-999::2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:-999:2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_end')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[999::2]
        result = self.run_smart_contract(engine, path, 'really_high_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:999:2]
        result = self.run_smart_contract(engine, path, 'really_high_end')
        self.assertEqual(expected_result, result)

    def test_string_slicing_omitted_with_negative_stride(self):
        path = self.get_contract_path('StringSlicingOmittedWithNegativeStride.py')
        engine = TestEngine()

        a = 'unit_test'
        expected_result = a[::-2]
        result = self.run_smart_contract(engine, path, 'omitted_values')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:5:-2]
        result = self.run_smart_contract(engine, path, 'omitted_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[2::-2]
        result = self.run_smart_contract(engine, path, 'omitted_end')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-6::-2]
        result = self.run_smart_contract(engine, path, 'negative_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:-1:-2]
        result = self.run_smart_contract(engine, path, 'negative_end')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[-999::-2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:-999:-2]
        result = self.run_smart_contract(engine, path, 'negative_really_low_end')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[999::-2]
        result = self.run_smart_contract(engine, path, 'really_high_start')
        self.assertEqual(expected_result, result)

        a = 'unit_test'
        expected_result = a[:999:-2]
        result = self.run_smart_contract(engine, path, 'really_high_end')
        self.assertEqual(expected_result, result)

    def test_string_simple_concat(self):
        path = self.get_contract_path('StringSimpleConcat.py')

        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual('bye worldhi', result)

    def test_boa2_string_concat_test(self):
        path = self.get_contract_path('ConcatBoa2Test.py')
        engine = TestEngine()
        result = self.run_smart_contract(engine, path, 'main')
        self.assertEqual('helloworld', result)

    def test_boa2_string_concat_test2(self):
        path = self.get_contract_path('ConcatBoa2Test2.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'main', 'concat', ['hello', 'world'])
        self.assertEqual('helloworld', result)

        result = self.run_smart_contract(engine, path, 'main', 'blah', ['hello', 'world'])
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', 'concat', ['blah'])
        self.assertEqual(False, result)

        result = self.run_smart_contract(engine, path, 'main', 'concat', ['hello', 'world', 'third'])
        self.assertEqual('helloworld', result)

        result = self.run_smart_contract(engine, path, 'main', 'concat', ['1', 'neo'])
        self.assertEqual('1neo', result)

        result = self.run_smart_contract(engine, path, 'main', 'concat', ['', 'neo'])
        self.assertEqual('neo', result)

    def test_string_with_double_quotes(self):
        path = self.get_contract_path('StringWithDoubleQuotes.py')
        engine = TestEngine()

        result = self.run_smart_contract(engine, path, 'string_test', 'hello', 'world')
        self.assertEqual('"hell"test_symbol":world}"', result)

        result = self.run_smart_contract(engine, path, 'string_test', '1', 'neo')
        self.assertEqual('""test_symbol":neo}"', result)

        result = self.run_smart_contract(engine, path, 'string_test', 'neo', '')
        self.assertEqual('"ne"test_symbol":}"', result)

    def test_string_upper(self):
        path = self.get_contract_path('UpperStringMethod.py')
        engine = TestEngine()

        string = 'abcdefghijklmnopqrstuvwxyz'
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.upper(), result)

        string = 'a1b123y3z'
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.upper(), result)

        string = '!@#$%123*-/'
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.upper(), result)

        string = 'áõèñ'
        result = self.run_smart_contract(engine, path, 'main', string)

        with self.assertRaises(AssertionError):
            # TODO: upper was implemented for ASCII characters only
            self.assertEqual(string.upper(), result)

    def test_string_lower(self):
        path = self.get_contract_path('LowerStringMethod.py')
        engine = TestEngine()

        string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.lower(), result)

        string = 'A1B123Y3Z'
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.lower(), result)

        string = '!@#$%123*-/'
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.lower(), result)

        string = 'ÁÕÈÑ'
        result = self.run_smart_contract(engine, path, 'main', string)

        with self.assertRaises(AssertionError):
            # TODO: lower was implemented for ASCII characters only
            self.assertEqual(string.lower(), result)

    def test_string_startswith_method(self):
        path = self.get_contract_path('StartswithStringMethod.py')
        engine = TestEngine()

        string = 'unit_test'
        substring = 'unit'
        start = 0
        end = len(string)
        result = self.run_smart_contract(engine, path, 'main', string, substring, start, end)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = 'unit'
        start = 2
        end = 6
        result = self.run_smart_contract(engine, path, 'main', string, substring, start, end)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = 'it'
        start = 2
        end = 6
        result = self.run_smart_contract(engine, path, 'main', string, substring, start, end)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = 'it'
        start = 2
        end = 3
        result = self.run_smart_contract(engine, path, 'main', string, substring, start, end)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = 'unit_tes'
        start = -99
        end = -1
        result = self.run_smart_contract(engine, path, 'main', string, substring, start, end)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = ''
        start = 0
        end = 0
        result = self.run_smart_contract(engine, path, 'main', string, substring, start, end)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = 'unit_test'
        start = 0
        end = 99
        result = self.run_smart_contract(engine, path, 'main', string, substring, start, end)
        self.assertEqual(string.startswith(substring, start, end), result)

        string = 'unit_test'
        substring = 'unit_test'
        start = 100
        end = 99
        result = self.run_smart_contract(engine, path, 'main', string, substring, start, end)
        self.assertEqual(string.startswith(substring, start, end), result)

    def test_string_startswith_method_default_end(self):
        path = self.get_contract_path('StartswithStringMethodDefaultEnd.py')
        engine = TestEngine()

        string = 'unit_test'
        substring = 'unit'
        start = 0
        result = self.run_smart_contract(engine, path, 'main', string, substring, start)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = 'unit'
        start = 2
        result = self.run_smart_contract(engine, path, 'main', string, substring, start)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = 'it'
        start = 2
        result = self.run_smart_contract(engine, path, 'main', string, substring, start)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = 'it'
        start = 3
        result = self.run_smart_contract(engine, path, 'main', string, substring, start)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = 'unit_tes'
        start = -99
        result = self.run_smart_contract(engine, path, 'main', string, substring, start)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = ''
        start = 0
        result = self.run_smart_contract(engine, path, 'main', string, substring, start)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = ''
        start = 99
        result = self.run_smart_contract(engine, path, 'main', string, substring, start)
        self.assertEqual(string.startswith(substring, start), result)

        string = 'unit_test'
        substring = 'unit_test'
        start = 0
        result = self.run_smart_contract(engine, path, 'main', string, substring, start)
        self.assertEqual(string.startswith(substring, start), result)

    def test_string_startswith_method_defaults(self):
        path = self.get_contract_path('StartswithStringMethodDefaults.py')
        engine = TestEngine()

        string = 'unit_test'
        substring = 'unit'
        result = self.run_smart_contract(engine, path, 'main', string, substring)
        self.assertEqual(string.startswith(substring), result)

        string = 'unit_test'
        substring = 'unit_test'
        result = self.run_smart_contract(engine, path, 'main', string, substring)
        self.assertEqual(string.startswith(substring), result)

        string = 'unit_test'
        substring = ''
        result = self.run_smart_contract(engine, path, 'main', string, substring)
        self.assertEqual(string.startswith(substring), result)

        string = 'unit_test'
        substring = '12345'
        result = self.run_smart_contract(engine, path, 'main', string, substring)
        self.assertEqual(string.startswith(substring), result)

        string = 'unit_test'
        substring = 'bigger substring'
        result = self.run_smart_contract(engine, path, 'main', string, substring)
        self.assertEqual(string.startswith(substring), result)

    def test_string_strip(self):
        path = self.get_contract_path('StripStringMethod.py')
        engine = TestEngine()

        string = 'abcdefghijklmnopqrstuvwxyz'
        chars = 'abcxyz'
        result = self.run_smart_contract(engine, path, 'main', string, chars)
        self.assertEqual(string.strip(chars), result)

        string = 'abcdefghijklmnopqrsvwxyz unit test abcdefghijklmnopqrsvwxyz'
        chars = 'abcdefghijklmnopqrsvwxyz '
        result = self.run_smart_contract(engine, path, 'main', string, chars)
        self.assertEqual(string.strip(chars), result)

        string = '0123456789hello world987654310'
        chars = '0987654321'
        result = self.run_smart_contract(engine, path, 'main', string, chars)
        self.assertEqual(string.strip(chars), result)

    def test_string_strip_default(self):
        path = self.get_contract_path('StripStringMethodDefault.py')
        engine = TestEngine()

        string = '     unit test    '
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.strip(), result)

        string = 'unit test    '
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.strip(), result)

        string = '    unit test'
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.strip(), result)

        string = ' \t\n\r\f\vunit test \t\n\r\f\v'
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.strip(), result)

    def test_isdigit_method(self):
        path = self.get_contract_path('IsdigitMethod.py')
        engine = TestEngine()

        string = '0123456789'
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.isdigit(), result)

        string = '23mixed01'
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.isdigit(), result)

        string = 'no digits here'
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.isdigit(), result)

        string = ''
        result = self.run_smart_contract(engine, path, 'main', string)
        self.assertEqual(string.isdigit(), result)

        string = '¹²³'
        result = self.run_smart_contract(engine, path, 'main', string)
        with self.assertRaises(AssertionError):
            # neo3-boas isdigit implementation does not verify values that are not from the ASCII
            self.assertEqual(string.isdigit(), result)

    def test_string_join_with_sequence(self):
        path = self.get_contract_path('JoinStringMethodWithSequence.py')
        engine = TestEngine()

        string = ' '
        sequence = ["Unit", "Test", "Neo3-boa"]
        result = self.run_smart_contract(engine, path, 'main', string, sequence)
        self.assertEqual(string.join(sequence), result)

        string = ' '
        sequence = []
        result = self.run_smart_contract(engine, path, 'main', string, sequence)
        self.assertEqual(string.join(sequence), result)

        string = ' '
        sequence = ["UnitTest"]
        result = self.run_smart_contract(engine, path, 'main', string, sequence)
        self.assertEqual(string.join(sequence), result)

    def test_string_join_with_dictionary(self):
        path = self.get_contract_path('JoinStringMethodWithDictionary.py')
        engine = TestEngine()

        string = ' '
        dictionary = {"Unit": 1, "Test": 2, "Neo3-boa": 3}
        result = self.run_smart_contract(engine, path, 'main', string, dictionary)
        self.assertEqual(string.join(dictionary), result)

        string = ' '
        dictionary = {}
        result = self.run_smart_contract(engine, path, 'main', string, dictionary)
        self.assertEqual(string.join(dictionary), result)

        string = ' '
        dictionary = {"UnitTest": 1}
        result = self.run_smart_contract(engine, path, 'main', string, dictionary)
        self.assertEqual(string.join(dictionary), result)

    def test_string_index(self):
        path = self.get_contract_path('IndexString.py')
        engine = TestEngine()

        string = 'unit test'
        substring = 'i'
        start = 0
        end = 4
        result = self.run_smart_contract(engine, path, 'main', string, substring, start, end)
        self.assertEqual(string.index(substring, start, end), result)

        string = 'unit test'
        substring = 'i'
        start = 2
        end = 4
        result = self.run_smart_contract(engine, path, 'main', string, substring, start, end)
        self.assertEqual(string.index(substring, start, end), result)

        with self.assertRaisesRegex(TestExecutionException, f'{self.SUBSTRING_NOT_FOUND_MSG}$'):
            self.run_smart_contract(engine, path, 'main', 'unit test', 'i', 3, 4)

        with self.assertRaisesRegex(TestExecutionException, f'{self.SUBSTRING_NOT_FOUND_MSG}$'):
            self.run_smart_contract(engine, path, 'main', 'unit test', 'i', 4, -1)

        with self.assertRaisesRegex(TestExecutionException, f'{self.SUBSTRING_NOT_FOUND_MSG}$'):
            self.run_smart_contract(engine, path, 'main', 'unit test', 'i', 0, -99)

        string = 'unit test'
        substring = 'i'
        start = 0
        end = -1
        result = self.run_smart_contract(engine, path, 'main', string, substring, start, end)
        self.assertEqual(string.index(substring, start, end), result)

        string = 'unit test'
        substring = 'n'
        start = 0
        end = 99
        result = self.run_smart_contract(engine, path, 'main', string, substring, start, end)
        self.assertEqual(string.index(substring, start, end), result)

    def test_string_index_end_default(self):
        path = self.get_contract_path('IndexStringEndDefault.py')
        engine = TestEngine()

        string = 'unit test'
        substring = 't'
        start = 0
        result = self.run_smart_contract(engine, path, 'main', string, substring, start)
        self.assertEqual(string.index(substring, start), result)

        string = 'unit test'
        substring = 't'
        start = 4
        result = self.run_smart_contract(engine, path, 'main', string, substring, start)
        self.assertEqual(string.index(substring, start), result)

        string = 'unit test'
        substring = 't'
        start = 6
        result = self.run_smart_contract(engine, path, 'main', string, substring, start)
        self.assertEqual(string.index(substring, start), result)

        with self.assertRaisesRegex(TestExecutionException, f'{self.SUBSTRING_NOT_FOUND_MSG}$'):
            self.run_smart_contract(engine, path, 'main', 'unit test', 'i', 99)

        with self.assertRaisesRegex(TestExecutionException, f'{self.SUBSTRING_NOT_FOUND_MSG}$'):
            self.run_smart_contract(engine, path, 'main', 'unit test', 't', -1)

        string = 'unit test'
        substring = 'i'
        start = -10
        result = self.run_smart_contract(engine, path, 'main', string, substring, start)
        self.assertEqual(string.index(substring, start), result)

    def test_string_index_defaults(self):
        path = self.get_contract_path('IndexStringDefaults.py')
        engine = TestEngine()

        string = 'unit test'
        substring = 'u'
        result = self.run_smart_contract(engine, path, 'main', string, substring)
        self.assertEqual(string.index(substring), result)

        string = 'unit test'
        substring = 't'
        result = self.run_smart_contract(engine, path, 'main', string, substring)
        self.assertEqual(string.index(substring), result)

        string = 'unit test'
        substring = ' '
        result = self.run_smart_contract(engine, path, 'main', string, substring)
        self.assertEqual(string.index(substring), result)

    def test_string_index_mismatched_type(self):
        path = self.get_contract_path('IndexStringMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
