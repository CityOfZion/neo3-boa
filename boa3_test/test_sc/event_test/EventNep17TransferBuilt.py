from boa3.sc.compiletime import public
from boa3.sc.types import UInt160
from boa3.sc.utils import CreateNewEvent

transfer = CreateNewEvent(
    [
        ('from', UInt160 | None),
        ('to', UInt160 | None),
        ('amount', int)
    ],
    'Transfer'
)


@public
def Main(from_addr: UInt160, to_addr: UInt160, amount: int):
    transfer(from_addr, to_addr, amount)
