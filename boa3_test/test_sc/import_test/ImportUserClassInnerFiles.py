from boa3.builtin.compile_time import public
from boa3_test.test_sc.import_test.class_import import ImportUserClass


@public
def build_example_object() -> str:
    return ImportUserClass.build_example_object().var_str
