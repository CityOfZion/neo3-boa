from typing import Union

from boa3.builtin import public


@public
def main(arg: Union[str, bool]) -> str:
    if isinstance(arg, str):
        # isinstance does not have semantic meaning yey, so this will fail
        # because the return is str and arg is Union[str, bool]
        return arg
    else:
        return 'boolean'
