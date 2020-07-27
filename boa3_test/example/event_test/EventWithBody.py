from boa3.builtin import event


@event
def Event(a: int):
    if a > 10:   # event's body is not compiled
        a = a % 10


def Main():
    Event(10)
