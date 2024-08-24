from typing import Set

from boa3.sc.compiletime import public


@public
def main() -> Set:
    return {'unit', 'test'}
