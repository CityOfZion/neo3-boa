from typing import List

from boa3.builtin import public, contract


@public
def main(number: int) -> List[int]:
    result_list: List[int] = []
    for x in range(number):
        idx: int = AnotherContract.return_zero()
        result_list.append(idx)
    return result_list


@contract('0xdd6eea9717f5467b7a9cb49dabce80d8b3700270')
class AnotherContract:

    @staticmethod
    def return_zero() -> int:
        pass
