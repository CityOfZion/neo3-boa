import module1
import module2

from boa3.builtin.compile_time import public


@public
def main() -> int:
    return 1 + module2.sample_method()


def sample_method() -> int:
    return module1.sample_method()
