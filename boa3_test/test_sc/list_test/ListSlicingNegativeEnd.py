from boa3.sc.compiletime import public


@public
def Main() -> list:
    a = [0, 1, 2, 3, 4, 5]
    return a[:-4]   # expect [0, 1]
