from boa3.sc.compiletime import public


@public
def main() -> int:
    d = {}

    d['a'] = 4
    d[13] = 3

    return d['a'] + d[13]
