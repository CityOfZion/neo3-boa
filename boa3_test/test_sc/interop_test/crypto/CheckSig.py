from boa3.builtin.compile_time import public
from boa3.builtin.interop.crypto import check_sig
from boa3.builtin.type import ECPoint


@public
def main() -> bool:
    pubkey: ECPoint = ECPoint(b'\x03\x5a\x92\x8f\x20\x16\x39\x20\x4e\x06\xb4\x36\x8b\x1a\x93\x36\x54\x62\xa8\xeb\xbf\xf0\xb8\x81\x81\x51\xb7\x4f\xaa\xb3\xa2\xb6\x1a')
    signature: bytes = b'wrongsignature'
    return check_sig(pubkey, signature)
