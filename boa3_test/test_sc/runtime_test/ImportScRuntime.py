from boa3 import sc
from boa3.sc.compiletime import public


@public
def main() -> int:
    return sc.runtime.get_trigger() + sc.runtime.get_trigger()
