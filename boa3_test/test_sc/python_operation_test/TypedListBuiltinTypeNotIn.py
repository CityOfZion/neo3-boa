from boa3.sc.compiletime import public
from boa3.sc.types import FindOptions


@public
def main(value: FindOptions, some_list: list[FindOptions]) -> bool:
    return value not in some_list
