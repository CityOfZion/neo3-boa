from boa3.sc.compiletime import public


@public
def main(string: str, old: str, new: str, count: int) -> str:
    return string.replace(old)
