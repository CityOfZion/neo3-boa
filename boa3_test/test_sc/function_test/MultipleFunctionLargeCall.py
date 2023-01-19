from typing import Any, List

from boa3.builtin.compile_time import public


@public
def main(operation: str, arg: List[int]) -> Any:
    if operation == 'calculate' and len(arg) >= 2:
        operands: List[int] = []
        i = 1
        while i < len(arg):
            operands.append(arg[i])
            i += 1
        return calculate(arg[0], operands)
    else:
        return None


@public
def calculate(op_id: int, operands: List[int]) -> Any:
    op = get_operation(op_id)
    result: Any
    if len(operands) <= 0:
        result = "There are missing some parameters..."
    else:
        calc = operands[0]
        y = 1
        size = len(operands)
        while y < size:
            calc = calculate_simple(op, calc, operands[y])
            y += 1
        else:
            result = calc
    return result


def get_operation(args: int) -> str:
    if args == 1:
        return "add"
    elif args == 2:
        return "sub"
    elif args == 3:
        return "div"
    elif args == 4:
        return "mul"
    elif args == 5:
        return "mod"
    else:
        return "Operation must be between 1 and 5"


def calculate_simple(operation: str, a: int, b: int) -> int:
    add_op = "add"
    sub_op = "sub"
    mul_op = "mul"
    div_op = "div"
    mod_op = "mod"

    if operation == add_op:
        return add(a, b)
    elif operation == sub_op:
        return sub(a, b)
    elif operation == div_op:
        return div(a, b)
    elif operation == mul_op:
        return mul(a, b)
    elif operation == mod_op:
        return mod(a, b)
    else:
        return 0


def sub(a: int, b: int) -> int:
    return a - b


def add(a: int, b: int) -> int:
    return a + b


def div(a: int, b: int) -> int:
    return a // b


def mul(a: int, b: int) -> int:
    return a * b


def mod(a: int, b: int) -> int:
    return a % b
