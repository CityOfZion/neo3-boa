from boa3.boa3 import Boa3
from boa3.internal.exception import CompilerError
from boa3.internal.neo.vm.opcode.Opcode import Opcode
from boa3.internal.neo.vm.type.Integer import Integer
from boa3.internal.neo.vm.type.String import String
from boa3.internal.neo3.vm import VMState
from boa3_test.test_drive.testrunner.neo_test_runner import NeoTestRunner
from boa3_test.tests.boa_test import BoaTest


class TestString(BoaTest):
    default_folder: str = 'test_sc/string_test'

    SUBSTRING_NOT_FOUND_MSG = 'substring not found'

    def test_string_get_value(self):
        path, _ = self.get_deploy_file_paths('GetValue.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 'unit'))
        expected_results.append('u')
        invokes.append(runner.call_contract(path, 'Main', '123'))
        expected_results.append('1')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', '')
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_string_get_value_to_variable(self):
        path, _ = self.get_deploy_file_paths('GetValueToVariable.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main', 'unit'))
        expected_results.append('u')
        invokes.append(runner.call_contract(path, 'Main', '123'))
        expected_results.append('1')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'Main', '')
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state)
        self.assertRegex(runner.error, self.VALUE_IS_OUT_OF_RANGE_MSG_REGEX_SUFFIX)

    def test_string_set_value(self):
        path = self.get_contract_path('SetValue.py')
        self.assertCompilerLogs(CompilerError.UnresolvedOperation, path)

    def test_string_slicing(self):
        path, _ = self.get_deploy_file_paths('StringSlicingLiteralValues.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append('i')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_slicing_start_larger_than_ending(self):
        path, _ = self.get_deploy_file_paths('StringSlicingStartLargerThanEnding.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append('')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_slicing_with_variables(self):
        path, _ = self.get_deploy_file_paths('StringSlicingVariableValues.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append('i')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_slicing_negative_start(self):
        path, _ = self.get_deploy_file_paths('StringSlicingNegativeStart.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(b'unit_')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_slicing_negative_end_omitted(self):
        path, _ = self.get_deploy_file_paths('StringSlicingNegativeEndOmitted.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append('test')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_slicing_start_omitted(self):
        path, _ = self.get_deploy_file_paths('StringSlicingStartOmitted.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(b'uni')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

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

        path, _ = self.get_deploy_file_paths(path)
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main'))
        expected_results.append('unit_test')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_slicing_end_omitted(self):
        path, _ = self.get_deploy_file_paths('StringSlicingEndOmitted.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'Main',
                                            expected_result_type=bytes))
        expected_results.append(b'it_test')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_slicing_with_stride(self):
        path, _ = self.get_deploy_file_paths('StringSlicingWithStride.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        a = 'unit_test'
        expected_result = a[2:5:2]
        invokes.append(runner.call_contract(path, 'literal_values'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[-6:5:2]
        invokes.append(runner.call_contract(path, 'negative_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[0:-1:2]
        invokes.append(runner.call_contract(path, 'negative_end'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[-6:-1:2]
        invokes.append(runner.call_contract(path, 'negative_values'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[-999:5:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[0:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[-999:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_values'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[999:5:2]
        invokes.append(runner.call_contract(path, 'really_high_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[0:999:2]
        invokes.append(runner.call_contract(path, 'really_high_end'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[999:999:2]
        invokes.append(runner.call_contract(path, 'really_high_values'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_slicing_with_negative_stride(self):
        path, _ = self.get_deploy_file_paths('StringSlicingWithNegativeStride.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        a = 'unit_test'
        expected_result = a[2:5:-1]
        invokes.append(runner.call_contract(path, 'literal_values'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[-6:5:-1]
        invokes.append(runner.call_contract(path, 'negative_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[0:-1:-1]
        invokes.append(runner.call_contract(path, 'negative_end'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[-6:-1:-1]
        invokes.append(runner.call_contract(path, 'negative_values'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[-999:5:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[0:-999:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_end'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[-999:-999:-1]
        invokes.append(runner.call_contract(path, 'negative_really_low_values'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[999:5:-1]
        invokes.append(runner.call_contract(path, 'really_high_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[0:999:-1]
        invokes.append(runner.call_contract(path, 'really_high_end'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[999:999:-1]
        invokes.append(runner.call_contract(path, 'really_high_values'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_slicing_omitted_with_stride(self):
        path, _ = self.get_deploy_file_paths('StringSlicingOmittedWithStride.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        a = 'unit_test'
        expected_result = a[::2]
        invokes.append(runner.call_contract(path, 'omitted_values'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[:5:2]
        invokes.append(runner.call_contract(path, 'omitted_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[2::2]
        invokes.append(runner.call_contract(path, 'omitted_end'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[-6::2]
        invokes.append(runner.call_contract(path, 'negative_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[:-1:2]
        invokes.append(runner.call_contract(path, 'negative_end'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[-999::2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[:-999:2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[999::2]
        invokes.append(runner.call_contract(path, 'really_high_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[:999:2]
        invokes.append(runner.call_contract(path, 'really_high_end'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_slicing_omitted_with_negative_stride(self):
        path, _ = self.get_deploy_file_paths('StringSlicingOmittedWithNegativeStride.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        a = 'unit_test'
        expected_result = a[::-2]
        invokes.append(runner.call_contract(path, 'omitted_values'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[:5:-2]
        invokes.append(runner.call_contract(path, 'omitted_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[2::-2]
        invokes.append(runner.call_contract(path, 'omitted_end'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[-6::-2]
        invokes.append(runner.call_contract(path, 'negative_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[:-1:-2]
        invokes.append(runner.call_contract(path, 'negative_end'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[-999::-2]
        invokes.append(runner.call_contract(path, 'negative_really_low_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[:-999:-2]
        invokes.append(runner.call_contract(path, 'negative_really_low_end'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[999::-2]
        invokes.append(runner.call_contract(path, 'really_high_start'))
        expected_results.append(expected_result)

        a = 'unit_test'
        expected_result = a[:999:-2]
        invokes.append(runner.call_contract(path, 'really_high_end'))
        expected_results.append(expected_result)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_simple_concat(self):
        path, _ = self.get_deploy_file_paths('StringSimpleConcat.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append('bye worldhi')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_string_concat_test(self):
        path, _ = self.get_deploy_file_paths('ConcatBoa2Test.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main'))
        expected_results.append('helloworld')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_boa2_string_concat_test2(self):
        path, _ = self.get_deploy_file_paths('ConcatBoa2Test2.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'main', 'concat', ['hello', 'world']))
        expected_results.append('helloworld')

        invokes.append(runner.call_contract(path, 'main', 'blah', ['hello', 'world']))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 'concat', ['blah']))
        expected_results.append(False)

        invokes.append(runner.call_contract(path, 'main', 'concat', ['hello', 'world', 'third']))
        expected_results.append('helloworld')

        invokes.append(runner.call_contract(path, 'main', 'concat', ['1', 'neo']))
        expected_results.append('1neo')

        invokes.append(runner.call_contract(path, 'main', 'concat', ['', 'neo']))
        expected_results.append('neo')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_with_double_quotes(self):
        path, _ = self.get_deploy_file_paths('StringWithDoubleQuotes.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        invokes.append(runner.call_contract(path, 'string_test', 'hello', 'world'))
        expected_results.append('"hell"test_symbol":world}"')

        invokes.append(runner.call_contract(path, 'string_test', '1', 'neo'))
        expected_results.append('""test_symbol":neo}"')

        invokes.append(runner.call_contract(path, 'string_test', 'neo', ''))
        expected_results.append('"ne"test_symbol":}"')

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_upper(self):
        path, _ = self.get_deploy_file_paths('UpperStringMethod.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = 'abcdefghijklmnopqrstuvwxyz'
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.upper())

        string = 'a1b123y3z'
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.upper())

        string = '!@#$%123*-/'
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.upper())

        string = 'áõèñ'
        not_as_expected = runner.call_contract(path, 'main', string)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # TODO: upper was implemented for ASCII characters only
        self.assertNotEqual(string.upper(), not_as_expected.result)

    def test_string_lower(self):
        path, _ = self.get_deploy_file_paths('LowerStringMethod.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.lower())

        string = 'A1B123Y3Z'
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.lower())

        string = '!@#$%123*-/'
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.lower())

        string = 'ÁÕÈÑ'
        not_as_expected = runner.call_contract(path, 'main', string)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # TODO: lower was implemented for ASCII characters only
        self.assertNotEqual(string.lower(), not_as_expected.result)

    def test_string_startswith_method(self):
        path, _ = self.get_deploy_file_paths('StartswithStringMethod.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = 'unit_test'
        substring = 'unit'
        start = 0
        end = len(string)
        invokes.append(runner.call_contract(path, 'main', string, substring, start, end))
        expected_results.append(string.startswith(substring, start, end))

        string = 'unit_test'
        substring = 'unit'
        start = 2
        end = 6
        invokes.append(runner.call_contract(path, 'main', string, substring, start, end))
        expected_results.append(string.startswith(substring, start, end))

        string = 'unit_test'
        substring = 'it'
        start = 2
        end = 6
        invokes.append(runner.call_contract(path, 'main', string, substring, start, end))
        expected_results.append(string.startswith(substring, start, end))

        string = 'unit_test'
        substring = 'it'
        start = 2
        end = 3
        invokes.append(runner.call_contract(path, 'main', string, substring, start, end))
        expected_results.append(string.startswith(substring, start, end))

        string = 'unit_test'
        substring = 'unit_tes'
        start = -99
        end = -1
        invokes.append(runner.call_contract(path, 'main', string, substring, start, end))
        expected_results.append(string.startswith(substring, start, end))

        string = 'unit_test'
        substring = ''
        start = 0
        end = 0
        invokes.append(runner.call_contract(path, 'main', string, substring, start, end))
        expected_results.append(string.startswith(substring, start, end))

        string = 'unit_test'
        substring = 'unit_test'
        start = 0
        end = 99
        invokes.append(runner.call_contract(path, 'main', string, substring, start, end))
        expected_results.append(string.startswith(substring, start, end))

        string = 'unit_test'
        substring = 'unit_test'
        start = 100
        end = 99
        invokes.append(runner.call_contract(path, 'main', string, substring, start, end))
        expected_results.append(string.startswith(substring, start, end))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_startswith_method_default_end(self):
        path, _ = self.get_deploy_file_paths('StartswithStringMethodDefaultEnd.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = 'unit_test'
        substring = 'unit'
        start = 0
        invokes.append(runner.call_contract(path, 'main', string, substring, start))
        expected_results.append(string.startswith(substring, start))

        string = 'unit_test'
        substring = 'unit'
        start = 2
        invokes.append(runner.call_contract(path, 'main', string, substring, start))
        expected_results.append(string.startswith(substring, start))

        string = 'unit_test'
        substring = 'it'
        start = 2
        invokes.append(runner.call_contract(path, 'main', string, substring, start))
        expected_results.append(string.startswith(substring, start))

        string = 'unit_test'
        substring = 'it'
        start = 3
        invokes.append(runner.call_contract(path, 'main', string, substring, start))
        expected_results.append(string.startswith(substring, start))

        string = 'unit_test'
        substring = 'unit_tes'
        start = -99
        invokes.append(runner.call_contract(path, 'main', string, substring, start))
        expected_results.append(string.startswith(substring, start))

        string = 'unit_test'
        substring = ''
        start = 0
        invokes.append(runner.call_contract(path, 'main', string, substring, start))
        expected_results.append(string.startswith(substring, start))

        string = 'unit_test'
        substring = ''
        start = 99
        invokes.append(runner.call_contract(path, 'main', string, substring, start))
        expected_results.append(string.startswith(substring, start))

        string = 'unit_test'
        substring = 'unit_test'
        start = 0
        invokes.append(runner.call_contract(path, 'main', string, substring, start))
        expected_results.append(string.startswith(substring, start))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_startswith_method_defaults(self):
        path, _ = self.get_deploy_file_paths('StartswithStringMethodDefaults.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = 'unit_test'
        substring = 'unit'
        invokes.append(runner.call_contract(path, 'main', string, substring))
        expected_results.append(string.startswith(substring))

        string = 'unit_test'
        substring = 'unit_test'
        invokes.append(runner.call_contract(path, 'main', string, substring))
        expected_results.append(string.startswith(substring))

        string = 'unit_test'
        substring = ''
        invokes.append(runner.call_contract(path, 'main', string, substring))
        expected_results.append(string.startswith(substring))

        string = 'unit_test'
        substring = '12345'
        invokes.append(runner.call_contract(path, 'main', string, substring))
        expected_results.append(string.startswith(substring))

        string = 'unit_test'
        substring = 'bigger substring'
        invokes.append(runner.call_contract(path, 'main', string, substring))
        expected_results.append(string.startswith(substring))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_strip(self):
        path, _ = self.get_deploy_file_paths('StripStringMethod.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = 'abcdefghijklmnopqrstuvwxyz'
        chars = 'abcxyz'
        invokes.append(runner.call_contract(path, 'main', string, chars))
        expected_results.append(string.strip(chars))

        string = 'abcdefghijklmnopqrsvwxyz unit test abcdefghijklmnopqrsvwxyz'
        chars = 'abcdefghijklmnopqrsvwxyz '
        invokes.append(runner.call_contract(path, 'main', string, chars))
        expected_results.append(string.strip(chars))

        string = '0123456789hello world987654310'
        chars = '0987654321'
        invokes.append(runner.call_contract(path, 'main', string, chars))
        expected_results.append(string.strip(chars))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_strip_default(self):
        path, _ = self.get_deploy_file_paths('StripStringMethodDefault.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = '     unit test    '
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.strip())

        string = 'unit test    '
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.strip())

        string = '    unit test'
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.strip())

        string = ' \t\n\r\f\vunit test \t\n\r\f\v'
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.strip())

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_isdigit_method(self):
        path, _ = self.get_deploy_file_paths('IsdigitMethod.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = '0123456789'
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.isdigit())

        string = '23mixed01'
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.isdigit())

        string = 'no digits here'
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.isdigit())

        string = ''
        invokes.append(runner.call_contract(path, 'main', string))
        expected_results.append(string.isdigit())

        string = '¹²³'
        not_as_expected = runner.call_contract(path, 'main', string)

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        # neo3-boas isdigit implementation does not verify values that are not from the ASCII
        self.assertNotEqual(string.isdigit(), not_as_expected.result)

    def test_string_join_with_sequence(self):
        path, _ = self.get_deploy_file_paths('JoinStringMethodWithSequence.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = ' '
        sequence = ["Unit", "Test", "Neo3-boa"]
        invokes.append(runner.call_contract(path, 'main', string, sequence))
        expected_results.append(string.join(sequence))

        string = ' '
        sequence = []
        invokes.append(runner.call_contract(path, 'main', string, sequence))
        expected_results.append(string.join(sequence))

        string = ' '
        sequence = ["UnitTest"]
        invokes.append(runner.call_contract(path, 'main', string, sequence))
        expected_results.append(string.join(sequence))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_join_with_dictionary(self):
        path, _ = self.get_deploy_file_paths('JoinStringMethodWithDictionary.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = ' '
        dictionary = {"Unit": 1, "Test": 2, "Neo3-boa": 3}
        invokes.append(runner.call_contract(path, 'main', string, dictionary))
        expected_results.append(string.join(dictionary))

        string = ' '
        dictionary = {}
        invokes.append(runner.call_contract(path, 'main', string, dictionary))
        expected_results.append(string.join(dictionary))

        string = ' '
        dictionary = {"UnitTest": 1}
        invokes.append(runner.call_contract(path, 'main', string, dictionary))
        expected_results.append(string.join(dictionary))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_index(self):
        path, _ = self.get_deploy_file_paths('IndexString.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = 'unit test'
        substring = 'i'
        start = 0
        end = 4
        invokes.append(runner.call_contract(path, 'main', string, substring, start, end))
        expected_results.append(string.index(substring, start, end))

        string = 'unit test'
        substring = 'i'
        start = 2
        end = 4
        invokes.append(runner.call_contract(path, 'main', string, substring, start, end))
        expected_results.append(string.index(substring, start, end))

        string = 'unit test'
        substring = 'i'
        start = 0
        end = -1
        invokes.append(runner.call_contract(path, 'main', string, substring, start, end))
        expected_results.append(string.index(substring, start, end))

        string = 'unit test'
        substring = 'n'
        start = 0
        end = 99
        invokes.append(runner.call_contract(path, 'main', string, substring, start, end))
        expected_results.append(string.index(substring, start, end))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', 'unit test', 'i', 3, 4)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state)
        self.assertRegex(runner.error, f'{self.SUBSTRING_NOT_FOUND_MSG}$')

        runner.call_contract(path, 'main', 'unit test', 'i', 4, -1)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state)
        self.assertRegex(runner.error, f'{self.SUBSTRING_NOT_FOUND_MSG}$')

        runner.call_contract(path, 'main', 'unit test', 'i', 0, -99)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state)
        self.assertRegex(runner.error, f'{self.SUBSTRING_NOT_FOUND_MSG}$')

    def test_string_index_end_default(self):
        path, _ = self.get_deploy_file_paths('IndexStringEndDefault.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = 'unit test'
        substring = 't'
        start = 0
        invokes.append(runner.call_contract(path, 'main', string, substring, start))
        expected_results.append(string.index(substring, start))

        string = 'unit test'
        substring = 't'
        start = 4
        invokes.append(runner.call_contract(path, 'main', string, substring, start))
        expected_results.append(string.index(substring, start))

        string = 'unit test'
        substring = 't'
        start = 6
        invokes.append(runner.call_contract(path, 'main', string, substring, start))
        expected_results.append(string.index(substring, start))

        string = 'unit test'
        substring = 'i'
        start = -10
        invokes.append(runner.call_contract(path, 'main', string, substring, start))
        expected_results.append(string.index(substring, start))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

        runner.call_contract(path, 'main', 'unit test', 'i', 99)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state)
        self.assertRegex(runner.error, f'{self.SUBSTRING_NOT_FOUND_MSG}$')

        runner.call_contract(path, 'main', 'unit test', 't', -1)
        runner.execute()

        self.assertEqual(VMState.FAULT, runner.vm_state)
        self.assertRegex(runner.error, f'{self.SUBSTRING_NOT_FOUND_MSG}$')

    def test_string_index_defaults(self):
        path, _ = self.get_deploy_file_paths('IndexStringDefaults.py')
        runner = NeoTestRunner()

        invokes = []
        expected_results = []

        string = 'unit test'
        substring = 'u'
        invokes.append(runner.call_contract(path, 'main', string, substring))
        expected_results.append(string.index(substring))

        string = 'unit test'
        substring = 't'
        invokes.append(runner.call_contract(path, 'main', string, substring))
        expected_results.append(string.index(substring))

        string = 'unit test'
        substring = ' '
        invokes.append(runner.call_contract(path, 'main', string, substring))
        expected_results.append(string.index(substring))

        runner.execute()
        self.assertEqual(VMState.HALT, runner.vm_state)

        for x in range(len(invokes)):
            self.assertEqual(expected_results[x], invokes[x].result)

    def test_string_index_mismatched_type(self):
        path = self.get_contract_path('IndexStringMismatchedType.py')
        self.assertCompilerLogs(CompilerError.MismatchedTypes, path)
