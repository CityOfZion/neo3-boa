def Main():
    any_list = [True, 1, 'ok']
    int_list = [1, 2, 3]
    any_tuple = (True, 1, 'ok')
    bool_tuple = True, False

    a: Sequence[Sequence[Any]] = [any_list, int_list, any_tuple, bool_tuple]
