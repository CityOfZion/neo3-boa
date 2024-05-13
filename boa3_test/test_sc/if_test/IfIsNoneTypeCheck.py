from boa3.sc import runtime
from boa3.sc.compiletime import public
from boa3.sc.contracts import GasToken


@public
def main(sample: bytes) -> bytes:
    if sample is not None:
        x = 10

    if sample is None and runtime.calling_script_hash != GasToken.hash:
        x = 20

    return sample
