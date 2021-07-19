from boa3.builtin import public


@public
def _deploy(is_updating: bool):
    if is_updating:
        return
