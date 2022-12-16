from boa3.builtin.compile_time import public


@public
def Main(condition: bool) -> int:
    if condition:
        if condition:
            if condition:
                return 1
            elif condition:
                return 2
            else:
                return 3
        elif condition:
            if condition:
                return 4
            else:
                return 5
        else:
            return 6
    else:
        if condition:
            return 7
        elif condition:
            return 8
        else:
            return 9
