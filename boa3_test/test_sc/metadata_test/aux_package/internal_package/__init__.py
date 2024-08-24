from boa3.sc.types import UInt160
from boa3.sc.utils import CreateNewEvent

on_transfer = CreateNewEvent(
    [
        ('from_addr', UInt160 | None),
        ('to_addr', UInt160 | None),
        ('amount', int),
    ],
    'Transfer'
)


def method_called(token_owner: UInt160 | None, to: UInt160 | None, amount: int):
    on_transfer(token_owner, to, amount)
