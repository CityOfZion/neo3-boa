from boa3.builtin.compile_time import public, contract


@public
def main(number: int) -> list[int]:
    result_list: list[int] = []
    for x in range(number):
        idx: int = AnotherContract.return_zero()
        result_list.append(idx)
    return result_list


@contract('0x48f74c68e8b538e62383085122367a030fe6441e')
class AnotherContract:

    @staticmethod
    def return_zero() -> int:
        pass
