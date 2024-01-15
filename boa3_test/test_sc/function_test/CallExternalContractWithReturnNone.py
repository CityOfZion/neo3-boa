from boa3.builtin.compile_time import contract, public


@contract('0x939e2bd39b8b5d1e7d77b64ea32c6ecbbbed578a')
class NoReturnContract:

    @staticmethod
    def Main(a: int):
        pass


@public
def main():
    NoReturnContract.Main(10)
