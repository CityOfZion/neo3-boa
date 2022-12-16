from boa3.builtin.compile_time import public


@public
def Main() -> bool:

    m = [2, 4, 1, 5 + 12]

    # we cant do this.  once you create an array you cant extend it
    # m[5] = 8

    m[2] = 7 + 10

    m2 = [9, 10, 11, 12]

    # we can change items
    m2[0] = 4

    # we can access items in the array!
    q = m[1]

    # m3 = m + m2 // VM wont support concatenating arrays for now

    # returns 1 aka true
    return m2[0] == q
