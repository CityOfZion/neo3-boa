from boa3.builtin.interop.contract import call_contract


def Main(scripthash: bytes, method: str):
    call_contract(scripthash, method)
