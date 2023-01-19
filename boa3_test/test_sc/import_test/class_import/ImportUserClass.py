from boa3.builtin.compile_time import public

from boa3_test.test_sc.import_test.class_import.example import Example


@public
def build_example_object() -> Example:
    return Example(42, '42')
