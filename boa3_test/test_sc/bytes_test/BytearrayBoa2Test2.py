from boa3.builtin.compile_time import public


@public
def main(ba1: bytearray, ba2: bytearray) -> bytearray:

    m = ba2[1:2]

    my_str = 'staoheustnau'

    m = my_str[3:5]

    m = ba1[1:len(ba1)]

    return m + my_str + ba2
