from boa3.builtin.compile_time import public


@public
def main() -> int:
    b = 1

    if None:
        b = b * 10
    if []:
        b = b * 10
    if {}:
        b = b * 10
    if ():
        b = b * 10

    if [1]:
        b = b + 1
    if {'a': 1}:
        b = b + 1
    if (1, 2):
        b = b + 1

    return b
