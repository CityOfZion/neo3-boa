from boa3.builtin.interop.contract import call_contract


def Main(scripthash: bytes, method: str, args: list):
    call_contract(scripthash, method, args)
