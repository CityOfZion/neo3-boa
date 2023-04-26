from boa3.builtin.compile_time import CreateNewEvent
from boa3.builtin.interop.iterator import Iterator

Event = CreateNewEvent(
    [
        ('a', Iterator)  # this shouldn't compile
    ]
)


def Main() -> bool:
    return False
