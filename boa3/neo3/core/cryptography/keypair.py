from __future__ import annotations

import bitcoin  # type: ignore

from boa3.neo3.core import cryptography


class KeyPair:
    def __init__(self, private_key: bytes):
        self.private_key = private_key
        self.public_key = None

        bitcoin.change_curve(
            115792089210356248762697446949407573530086143415290314195533631308867097853951,
            115792089210356248762697446949407573529996955224135760342422259061068512044369,
            115792089210356248762697446949407573530086143415290314195533631308867097853948,
            41058363725152142129326129780047268409114441015993725554835256314039467401291,
            48439561293906451759052585252797914202762949526041747995844080717082404635286,
            36134250956749795798585127919587881956611106672985015071877198253568414405109
        )

        length = len(self.private_key)

        if length != 32:
            raise ValueError("Invalid private key")

        if length == 32:
            try:
                pubkey_encoded_not_compressed = bitcoin.privkey_to_pubkey(private_key)
                pubkey_points = bitcoin.decode_pubkey(pubkey_encoded_not_compressed, 'bin')

                pubx = pubkey_points[0]
                puby = pubkey_points[1]
                self.public_key = cryptography.ECDSA.secp256r1().Curve.point(pubx, puby)
            except Exception:
                raise ValueError("Could not determine public key")
