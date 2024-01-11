from boa3.builtin.compile_time import public


@public
def main(operation: int) -> bool:

    if operation == 1:

        a = 'test_string'
        b = bytearray(b'test_byte_array')

        return a == b

    elif operation == 2:

        a = bytearray(b'unit_test')
        b = 'unit_test'

        return a == b

    elif operation == 3:

        a = b'test_bytes'
        b = 'test_string'
        return a == b

    elif operation == 4:

        a = 0
        b = False
        return a == b

    elif operation == 5:

        a = 0
        b = ''
        return a == b

    elif operation == 6:

        a = False
        b = ''
        return a == b

    elif operation == 7:

        a = False
        b = b''
        return a == b

    return False
