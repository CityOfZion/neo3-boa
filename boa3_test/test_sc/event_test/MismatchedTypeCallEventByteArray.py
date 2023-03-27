from boa3.builtin.compile_time import CreateNewEvent


Event = CreateNewEvent(
    [
        ('a', bytes)
    ]
)


def Main():
    Event('10')
