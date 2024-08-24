from boa3.sc.compiletime import public


@public
def main() -> str:
    return min('Lorem', 'ipsum', 'dolor', 'sit', 'amet')
