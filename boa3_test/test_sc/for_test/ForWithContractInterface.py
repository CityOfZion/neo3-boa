from typing import List

from boa3.builtin.compile_time import public, contract


@public
def main(number: int) -> List[int]:
    result_list: List[int] = []
    for x in range(number):
        idx: int = AnotherContract.return_zero()
        result_list.append(idx)
    return result_list


@contract('0x1330b4cebb77680e29949ec34669dcdd89280671')
class AnotherContract:

    @staticmethod
    def return_zero() -> int:
        pass
