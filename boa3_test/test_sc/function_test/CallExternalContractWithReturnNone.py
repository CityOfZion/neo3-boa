from boa3.builtin.compile_time import contract, public


@contract('0xcd8fe0d1ba2619fc05a1234edc22a6bae363f119')
class NoReturnContract:

    @staticmethod
    def Main(a: int):
        pass


@public
def main():
    NoReturnContract.Main(10)
