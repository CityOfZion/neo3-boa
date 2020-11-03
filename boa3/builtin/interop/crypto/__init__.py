from typing import Any, List


def sha256(key: Any) -> bytes:
    pass


def ripemd160(key: Any) -> bytes:
    pass


def hash160(key: Any) -> bytes:
    pass


def hash256(key: Any) -> bytes:
    pass


def check_multisig_with_ecdsa_secp256r1(item: Any, pubkeys: List[bytes], signatures: List[bytes]) -> bool:
    pass


def check_multisig_with_ecdsa_secp256k1(item: Any, pubkeys: List[bytes], signatures: List[bytes]) -> bool:
    pass
