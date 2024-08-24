from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken
from boa3.sc.utils.iterator import Iterator


@public
def main() -> Iterator:
    return NeoToken.get_all_candidates()
