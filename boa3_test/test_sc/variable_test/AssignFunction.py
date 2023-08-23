from boa3.builtin.compile_time import public


@public
def function() -> int:
    return 123


@public
def main() -> int:
    a = function
    return a()
