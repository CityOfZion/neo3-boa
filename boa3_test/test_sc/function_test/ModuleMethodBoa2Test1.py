from boa3.builtin import public
from boa3.builtin.interop.crypto import sha256

MYSHA = sha256('abc')


@public
def main() -> bool:

    m = 3

    j2 = sha256('abc')

    j3 = MYSHA

#    print(j2)

    return j2 == j3
