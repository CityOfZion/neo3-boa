from .sample_package.package import sample_module   # , another_module
# from boa3_test.test_sc.import_test.sample_package.package import sample_module

# def call_imported_method() -> list:
#     a: sample_module.List[sample_module.Any] = sample_module.EmptyList()
#     return a


def call_imported_variable() -> list:
    return sample_module.empty_list

