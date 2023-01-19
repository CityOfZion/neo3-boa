from boa3.builtin.compile_time import public


@public
def main(operation: str, idx1: int, idx2: int) -> int:

    mylist = [1, 2, 3, 5, 9, 1000, 32, -1]

    mystr_list = ['ab', 'bc', 'de', 'ef']

    if operation == 'add':

        return mylist[idx1] + mylist[idx2]

    elif operation == 'sub':

        return mylist[idx1] - mylist[idx2]

    elif operation == 'fun':

        return my_method(my_method_2(mylist[idx1]), my_method_3(mylist[idx2]))

    return False


def my_method(a: int, b: int) -> int:

    return a + b


def my_method_2(c: int) -> int:

    return c * 2


def my_method_3(j: int) -> int:

    return j + 1
