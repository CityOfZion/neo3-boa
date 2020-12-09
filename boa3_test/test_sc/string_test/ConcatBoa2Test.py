from boa3.builtin import public


@public
def main() -> str:
    str1 = 'hello'
    str2 = 'world'
    str3 = str1 + str2
    return str3
