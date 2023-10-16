from boa3.builtin.compile_time import public


@public
def get_list() -> list:
    x = [l for l in 'word']
    return x
