# tested
from boa3.builtin.compile_time import public, CreateNewEvent

Transfer = CreateNewEvent([('from', int), ('to', int), ('amount', int)], 'transfer_test')

Refund = CreateNewEvent([('to', str), ('amount', int)], 'refund')


@public
def main() -> int:

    a = 2

    b = 5

    c = a + b

    Transfer(a, b, c)

    to = 'me'
    amount = 52

    Refund(to, amount)

    return c
