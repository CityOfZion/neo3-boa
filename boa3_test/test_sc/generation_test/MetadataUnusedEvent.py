from boa3.builtin import public, CreateNewEvent
from boa3.builtin.interop.runtime import notify
uncalled_event = CreateNewEvent(
    [
        ('var1', int),
        ('var2', int),
        ('var3', int)
    ],
    'UncalledEvent'
)

called_event = CreateNewEvent(
    [
        ('var4', int),
        ('var5', str),
        ('var6', bytes)
    ],
    'CalledEvent'
)


@public
def main(a: int, b: int) -> int:
    called_event(1, '1', b'1')
    return a + b
