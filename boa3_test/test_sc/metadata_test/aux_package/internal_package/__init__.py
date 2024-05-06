from boa3.builtin.compile_time import CreateNewEvent
from boa3.builtin.type import UInt160

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
