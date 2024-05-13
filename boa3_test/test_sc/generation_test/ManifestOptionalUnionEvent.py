from boa3.sc.compiletime import public
from boa3.sc.utils import CreateNewEvent


event = CreateNewEvent(
    [
        ('optional', str | None),
        ('union', int | None),
        ('union2', bool | None)
    ],
    'event'
)


@public
def main():
    event('foo', 1, True)
