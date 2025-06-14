from boa3.sc.compiletime import public
from boa3.sc.types import ECPoint
from boa3.sc.utils import check_multisig


@public
def main() -> bool:
    pubkeys: list[ECPoint] = [ECPoint(b'\x03\xcd\xb0g\xd90\xfdZ\xda\xa6\xc6\x85E\x01`D\xaa\xdd\xecd\xba9\xe5H%\x0e\xae\xa5Q\x17.S\\'),
                              ECPoint(b'\x03l\x841\xccx\xb31w\xa6\x0bK\xcc\x02\xba\xf6\r\x05\xfe\xe5\x03\x8es9\xd3\xa6\x88\xe3\x94\xc2\xcb\xd8C')]
    signatures: list[bytes] = [b'wrongsignature1', b'wrongsignature2']
    return check_multisig(pubkeys, signatures)
