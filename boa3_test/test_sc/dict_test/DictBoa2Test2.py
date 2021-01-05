from boa3.builtin import public


@public
def Main() -> int:

    d = {'b': 3, 42: 10 + 7}

    d['a'] = 4
    d[13] = 3

    return d['a'] + d[13]
