from typing import Union

from boa3.builtin.compile_time import CreateNewEvent
from boa3.builtin.type import UInt160

on_transfer = CreateNewEvent(
    [
        ('from_addr', Union[UInt160, None]),
        ('to_addr', Union[UInt160, None]),
        ('amount', int),
    ],
    'Transfer'
)


def method_called(token_owner: Union[UInt160, None], to: Union[UInt160, None], amount: int):
    on_transfer(token_owner, to, amount)
