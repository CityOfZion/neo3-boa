import base58


def address_to_script_hash(address: str, account_version: int = None) -> bytes:
    data = base58.b58decode_check(address)
    if isinstance(account_version, int):
        assert data[0] == account_version, "Address version doesn't match"

    return data[1:]  # first position is address version


def address_from_script_hash(script_hash: bytes, account_version: int) -> str:
    data = bytearray(script_hash)
    data.insert(0, account_version)

    return base58.b58encode_check(data).decode(encoding='utf-8')
