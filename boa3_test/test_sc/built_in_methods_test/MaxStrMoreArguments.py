from boa3.builtin import public


@public
def main() -> str:
    return max('Lorem', 'ipsum', 'dolor', 'sit', 'amet')
