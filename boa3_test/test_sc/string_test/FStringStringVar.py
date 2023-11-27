from boa3.builtin.compile_time import public


@public
def main(a: str) -> str:
    fstring = f"F-string: {a}"
    return fstring
