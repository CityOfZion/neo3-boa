from boa3.builtin.compile_time import public


@public
def main(a: list) -> str:
    fstring = f"F-string: {a}"
    return fstring
