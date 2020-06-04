def Main():
    bool_tuple = True, False

    SequenceFunction(bool_tuple)
    SequenceFunction([True, 1, 'ok'])
    SequenceFunction('some_string')
    SequenceFunction((True, 1, 'ok'))
    SequenceFunction([1, 2, 3])


def SequenceFunction(sequence: Sequence[Any]):
    a = sequence
