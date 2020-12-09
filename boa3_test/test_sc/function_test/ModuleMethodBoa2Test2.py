from boa3.builtin import public


BLAH = 10 * 300

# This wont work
# BLAH2 = BLAH * 100


@public
def main() -> int:

    m = 3

    j = m + BLAH

    return j
