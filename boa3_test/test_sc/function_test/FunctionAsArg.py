from boa3.builtin import public


@public
def main(value: int) -> int:
    var = return_int(value.to_bytes())

    return var


def return_int(arg1: bytes) -> int:
    return arg1.to_int()
