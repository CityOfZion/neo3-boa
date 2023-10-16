from typing import Set

from boa3.builtin.compile_time import public


@public
def main() -> Set:
    return {'unit', 'test'}
