from boa3.builtin import public


@public
def Main() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[:3]   # expect [0, 1, 2]
