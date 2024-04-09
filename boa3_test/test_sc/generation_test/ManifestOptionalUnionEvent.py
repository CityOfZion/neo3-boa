from typing import Optional, Union

from boa3.builtin.compile_time import public, CreateNewEvent

event = CreateNewEvent(
    [
        ('optional', Optional[str]),
        ('union', Union[int, None]),
        ('union2', bool | None)
    ],
    'event'
)


@public
def main():
    event('foo', 1, True)
