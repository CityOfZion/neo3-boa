from boa3.sc.compiletime import public


@public
def _deploy(is_updating: bool):
    if is_updating:
        return
