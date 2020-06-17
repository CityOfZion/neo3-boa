def Main(condition1: bool, condition2: bool) -> int:
    if condition1:
        return 10
    elif condition2:
        return 20
    # when return type is not None in the signature, returns the default value of the type
    # in this example, it will return 0 if both `condition1` and `condition2` are False
