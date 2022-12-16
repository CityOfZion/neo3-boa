from typing import Any

from boa3.builtin.compile_time import public


@public
def main() -> Any:

    m = [[1, 2, 3], 'fun', 'cool', ['a', 'b', 'c']]

    answer = m[0]

    sub = m[3]

    sublen = len(sub)
    subitem = sub[0]

    return answer
