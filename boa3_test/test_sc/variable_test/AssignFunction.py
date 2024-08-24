from boa3.sc.compiletime import public


@public
def function() -> int:
    return 123


@public
def main() -> int:
    a = function
    return a()
