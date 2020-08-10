from typing import Dict


def Main(a: Dict[int, str]) -> Dict[int, str]:
    a[0] = 'ok'
    return a
