from boa3.sc.compiletime import public


@public
def get_list() -> list:
    x = [l for l in 'word']
    return x
