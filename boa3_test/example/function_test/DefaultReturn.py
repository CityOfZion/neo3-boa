def Main(condition1: bool, condition2: bool) -> int:
    if condition1:
        return 10
    elif condition2:
        return 20
    # this will raise a compiler error because there is a execution flow without a return statement
    # in this example, this flow is when both `condition1` and `condition2` are False
