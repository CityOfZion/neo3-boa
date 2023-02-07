from typing import List

from boa3.builtin.compile_time import public, contract


@public
def main(number: int) -> List[int]:
    result_list: List[int] = []
    for x in range(number):
        idx: int = AnotherContract.return_zero()
        result_list.append(idx)
    return result_list


@contract('0x5cb5e1b45b64e343ae79ded04f670b3770eadf48')
class AnotherContract:

    @staticmethod
    def return_zero() -> int:
        pass
