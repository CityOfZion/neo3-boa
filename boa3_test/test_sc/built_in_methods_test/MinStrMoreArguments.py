from boa3.builtin import public


@public
def main() -> str:
    return min('Lorem', 'ipsum', 'dolor', 'sit', 'amet')
