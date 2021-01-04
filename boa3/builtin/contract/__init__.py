from boa3.builtin import CreateNewEvent
from boa3.builtin.type import UInt160

Nep5TransferEvent = CreateNewEvent(
    [
        ('from_addr', bytes),
        ('to_addr', bytes),
        ('amount', int)
    ],
    'transfer'
)

Nep17TransferEvent = CreateNewEvent(
    [
        ('from_addr', UInt160),
        ('to_addr', UInt160),
        ('amount', int)
    ],
    'Transfer'
)


def abort():
    """
    Abort the execution of a smart contract
    """
    pass


def exit():
    """
    Abort the execution of a smart contract
    """
    pass
