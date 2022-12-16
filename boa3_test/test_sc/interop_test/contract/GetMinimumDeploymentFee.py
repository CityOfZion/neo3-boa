from boa3.builtin.compile_time import public
from boa3.builtin.interop.contract import get_minimum_deployment_fee


@public
def main() -> int:
    return get_minimum_deployment_fee()
