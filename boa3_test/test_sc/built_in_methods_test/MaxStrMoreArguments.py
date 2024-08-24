from boa3.sc.compiletime import public


@public
def main() -> str:
    return max('Lorem', 'ipsum', 'dolor', 'sit', 'amet')
