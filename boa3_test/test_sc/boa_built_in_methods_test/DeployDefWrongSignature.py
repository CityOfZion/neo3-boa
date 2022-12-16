from boa3.builtin.compile_time import public


@public
def _deploy(is_updating: bool):
    if is_updating:
        return
