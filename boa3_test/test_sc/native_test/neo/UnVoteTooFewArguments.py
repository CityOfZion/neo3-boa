from boa3.sc.compiletime import public
from boa3.sc.contracts import NeoToken


@public
def un_vote() -> bool:
    return NeoToken.un_vote()
