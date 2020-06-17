def Main(condition: bool) -> int:
    if condition:
        return 10
    else:
        return '10'  # compiler error - expecting int
