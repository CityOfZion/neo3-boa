from boa3.builtin.compile_time import public


@public
def main(operation: str, a: int, b: int) -> int | str:

    if operation == '&':
        return a & b
    elif operation == '|':
        return a | b
    elif operation == '^':
        return a ^ b
    elif operation == '>>':
        return a >> b
    elif operation == '%':
        return a % b
    elif operation == '//':
        return a // b
    elif operation == '~':
        return ~a
    return 'unknown'
