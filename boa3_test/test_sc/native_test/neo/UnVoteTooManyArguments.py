from boa3.builtin.compile_time import public
from boa3.builtin.nativecontract.neo import NEO
from boa3.builtin.type import UInt160


@public
def un_vote(account: UInt160) -> bool:
    return NEO.un_vote(account, None)
