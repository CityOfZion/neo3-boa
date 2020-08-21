from boa3.builtin import CreateNewEvent

Nep5TransferEvent = CreateNewEvent(
    [
        ('from_addr', bytes),
        ('to_addr', bytes),
        ('amount', int)
    ],
    'transfer'
)
