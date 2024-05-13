from boa3.sc.compiletime import public
from boa3.sc.runtime import get_random


@public
def main() -> int:
    return get_random()
