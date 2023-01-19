from typing import List, Dict, Union

from boa3.builtin.compile_time import public


@public
def Main(var: Dict[str, List[bool]]) -> List[Union[Dict[str, int], str, bool]]:
    if var:
        return []
    return []
