from typing import Union

from boa3.builtin.compile_time import public


@public
def main(operation: str, args: list[str]) -> Union[str, bool]:
    if operation == 'concat':
        return do_concat(args)
    else:
        return False


def do_concat(args: list[str]) -> Union[str, bool]:
    if len(args) > 1:
        a = args[0]
        b = args[1]
        output = a + b
        return output
    return False
