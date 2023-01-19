from boa3.builtin.compile_time import public


@public
def main() -> int:
    d = {}

    d['a'] = 4
    d[13] = 3

    return d['a'] + d[13]
