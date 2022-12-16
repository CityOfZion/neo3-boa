from boa3.builtin.compile_time import public


@public
def string_test(str1: str, str2: str) -> str:
    return '"' + str1[:-1] + '"test_symbol":' + str2 + '}"'
