from .ecc import (EllipticCurve, ECDSA)  # type: ignore
from .merkletree import MerkleTree
from .bloomfilter import BloomFilter
from bitcoin import (  # type: ignore
    decompress as bitcoin_decompress,
    change_curve as bitcoin_change_curve,
    ecdsa_raw_sign as bitcoin_ecdsa_raw_sign)
from .keypair import KeyPair
import ecdsa as _ecdsa  # type: ignore
import hashlib


__all__ = ['EllipticCurve', 'ECDSA', 'MerkleTree', 'BloomFilter', 'KeyPair']


def verify_signature(message: bytes, signature: bytes, encoded_pub_key_bytes) -> bool:
    length = len(encoded_pub_key_bytes)
    if length != 33 and (encoded_pub_key_bytes[0] == 0x2 or encoded_pub_key_bytes[0] == 0x3):
        pubkey = bitcoin_decompress(encoded_pub_key_bytes)
    elif length == 65 and encoded_pub_key_bytes[0] == 0x4:
        pubkey = encoded_pub_key_bytes[1:]
    elif length != 64:
        raise ValueError("Invalid public key bytes")

    # TODO: replace the _ecdsa module usage with verifications from own ECC lib.
    #  For time reasons use the old 2.x tested logic
    # note that NIST256P == secp256r1, so we should be able to use ECDSA.secp256r1().verify() or re-use the bitcoin
    # package. There is also an bitcoin.ecsa_raw_verify that probably can work.
    try:
        vk = _ecdsa.VerifyingKey.from_string(pubkey, curve=_ecdsa.NIST256p, hashfunc=hashlib.sha256)
        res = vk.verify(signature, message, hashfunc=hashlib.sha256)
        return res
    except Exception:
        pass
    return False


def sign(message: bytes, private_key: bytes) -> bytes:
    bitcoin_change_curve(
        115792089210356248762697446949407573530086143415290314195533631308867097853951,
        115792089210356248762697446949407573529996955224135760342422259061068512044369,
        115792089210356248762697446949407573530086143415290314195533631308867097853948,
        41058363725152142129326129780047268409114441015993725554835256314039467401291,
        48439561293906451759052585252797914202762949526041747995844080717082404635286,
        36134250956749795798585127919587881956611106672985015071877198253568414405109
    )
    hash_ = hashlib.sha256(message).hexdigest()
    v, r, s = bitcoin_ecdsa_raw_sign(hash_, private_key)
    rb = r.to_bytes(32, 'big')
    sb = s.to_bytes(32, 'big')

    sig = rb + sb
    return sig
