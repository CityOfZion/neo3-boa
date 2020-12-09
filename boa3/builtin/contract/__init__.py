from boa3.builtin import CreateNewEvent

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
        ('from_addr', bytes),   # TODO: change bytes to hash160 when possible
        ('to_addr', bytes),   # TODO: change bytes to hash160 when possible
        ('amount', int)
    ],
    'transfer'
)


def abort():
    """
    Abort the execution of a smart contract
    """
    pass
