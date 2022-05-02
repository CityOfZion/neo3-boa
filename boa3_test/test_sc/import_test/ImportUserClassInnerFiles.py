from boa3.builtin import public
from boa3_test.test_sc.import_test.class_import import ImportUserClass
# TODO: remove when the bug that doesn't initialize global variables from modules that are not imported in the main
#  file is fixed
import boa3_test.test_sc.import_test.class_import.example


@public
def build_example_object() -> str:
    return ImportUserClass.build_example_object().var_str
