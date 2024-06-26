from boa3.builtin.compile_time import public, CreateNewEvent
from boa3.builtin.type import UInt160

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
