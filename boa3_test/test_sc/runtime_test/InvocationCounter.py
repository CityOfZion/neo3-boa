from boa3.sc.compiletime import public
from boa3.sc.runtime import invocation_counter


@public
def Main() -> int:
    return invocation_counter
