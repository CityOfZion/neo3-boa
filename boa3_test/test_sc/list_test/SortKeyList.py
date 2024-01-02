def sort_test() -> list:
    a = [1, 2, 3, 4, 5]
    a.sort(key=key_order)
    return a


def key_order(n: int) -> int:
    return n % 5
