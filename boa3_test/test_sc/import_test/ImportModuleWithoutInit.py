from boa3.builtin.compile_time import public

from boa3_test.test_sc.import_test.sample_package.package import another_module, sample_module


@public
def call_imported_method() -> dict:
    a: another_module.Dict[another_module.Any, another_module.Any] = another_module.EmptyDict()
    return a


@public
def call_imported_variable() -> list:
    return sample_module.empty_list
