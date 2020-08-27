def Main(a: bool) -> int:
    a[0] = 1  # expecting mutable sequence
    return a
