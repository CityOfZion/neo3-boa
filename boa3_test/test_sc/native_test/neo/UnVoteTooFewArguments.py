from boa3.builtin import public
from boa3.builtin.nativecontract.neo import NEO


@public
def un_vote() -> bool:
    return NEO.un_vote()
