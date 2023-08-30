# Inner Functions are currently not allowed in smart contracts
def main() -> str:

    def inner_function() -> str:
        return 'unit test'

    return inner_function()
