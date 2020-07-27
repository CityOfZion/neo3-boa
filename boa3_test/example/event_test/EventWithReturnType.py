from boa3.builtin import event


@event
def Event() -> int:  # events must not have return type
    pass


def Main():
    Event()
