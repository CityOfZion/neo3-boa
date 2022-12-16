from boa3.builtin.compile_time import public


@public
def main() -> str:
    return min('Lorem', 'ipsum', 'dolor', 'sit', 'amet')
