from boa3.builtin.compile_time import public


@public
def test1(param: str) -> bool:
    return param[0:1] == '|'


@public
def test2(param: str) -> bool:
    return param[0:1] == "|"


@public
def test3(param: str) -> bool:
    return param == "|"


@public
def test4(param: str) -> bool:
    return param == '|'
