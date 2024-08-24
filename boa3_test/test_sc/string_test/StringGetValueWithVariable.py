from boa3.sc.compiletime import public


@public
def main(a: int) -> str:
    return 'test'[a]
