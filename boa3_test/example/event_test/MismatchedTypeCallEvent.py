from boa3.builtin import event


@event
def Event(a: int):
    pass


def Main():
    Event('10')
