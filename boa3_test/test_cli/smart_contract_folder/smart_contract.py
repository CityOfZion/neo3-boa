from boa3.builtin import env
from boa3.builtin.compile_time import public


@public
def main() -> str:
    return env
