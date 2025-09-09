from boa3.sc.compiletime import public
from boa3.sc.runtime import get_current_signers
from boa3.sc.types import Signer


@public
def main() -> list[Signer]:
    return get_current_signers()


@public
def compare_scope(s: int) -> bool:
    current_signers = get_current_signers()

    signer_scope = current_signers[0].scopes

    return signer_scope == s
