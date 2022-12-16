from typing import Dict

from boa3.builtin.compile_time import public


@public
def Main():
    a: Dict[int, Dict[int, bool]] = {
        1: {
            14: False,
            12: True,
            5: True
        },
        2: {
            0: True,
            6: False
        },
        3: {
            11: False
        }
    }
