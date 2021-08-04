from boa3.builtin import public


@public
def Main() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[0:5:-2]    # expected []
