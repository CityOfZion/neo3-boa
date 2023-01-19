from boa3.builtin.compile_time import public
from boa3.builtin.interop.runtime import notify


@public
def main() -> bytes:

    m = b'\x01\x02\x03\x04\x05\x06\x07\x08'

    s2 = m[:4]

    j = 2
    k = 4

    s3 = m[j:k]

    notify(s3)

    s4 = m[get_slice_start():get_slice_end()]

    notify(s4)

    ind = [1, 3, 4, 5]

    s6 = m[get_slice_start():ind[2]]

    notify(s6)

    res = s6 + s4 + s2 + s3

    notify(res)

    return res


def get_slice_start() -> int:

    return 1


def get_slice_end() -> int:
    return 6
