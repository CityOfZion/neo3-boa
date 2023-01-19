from boa3.builtin.compile_time import public


class Example:
    def __init__(self, value: int = 0):
        self.value = value

    def increase(self):
        self.value += 1

    def decrease(self):
        self.value -= 1

    def multiply(self):
        self.value *= 2

    def divide(self):
        self.value //= 2

    def modulo(self):
        self.value %= 2


@public
def add() -> int:
    var = Example()

    var.increase()  # 0 + 1 = 1
    var.increase()  # 1 + 1 = 2

    return var.value


@public
def sub() -> int:
    var = Example()

    var.decrease()  # 0 - 1 = -1
    var.decrease()  # -1 - 1 = -2

    return var.value


@public
def mult() -> int:
    var = Example(4)

    var.multiply()  # 4 * 2 = 8
    var.multiply()  # 8 * 2 = 16

    return var.value


@public
def div() -> int:
    var = Example(8)

    var.divide()    # 8 // 2 = 4
    var.divide()    # 4 // 2 = 2

    return var.value


@public
def mod() -> int:
    var = Example(9)

    var.modulo()    # 9 % 2 = 1

    return var.value


@public
def mix() -> int:
    var = Example(10)

    var.increase()  # 10 + 1 = 11
    var.multiply()  # 11 * 2 = 22
    var.decrease()  # 22 - 1 = 21
    var.modulo()    # 21 % 2 = 1
    var.divide()    # 1 // 2 = 0

    return var.value
