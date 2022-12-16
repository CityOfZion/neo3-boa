from boa3.builtin.compile_time import public
from boa3.builtin.interop import runtime
from boa3.builtin.interop.contract import GAS as GAS_SCRIPT


@public
def main(sample: bytes) -> bytes:
    if sample is not None:
        x = 10

    if sample is None and runtime.calling_script_hash != GAS_SCRIPT:
        x = 20

    return sample
