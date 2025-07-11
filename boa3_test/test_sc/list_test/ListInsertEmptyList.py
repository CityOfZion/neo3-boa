from boa3.sc.compiletime import public


@public
def main(index: int, number: int) -> list[int]:
    empty_list: list[int] = []

    empty_list.insert(index, number)
    return empty_list
