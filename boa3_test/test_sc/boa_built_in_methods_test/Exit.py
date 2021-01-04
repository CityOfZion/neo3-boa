from boa3.builtin import public
from boa3.builtin.contract import exit


@public
def main(check: bool) -> int:
    if check:
        exit()
    return 123
