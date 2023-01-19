from boa3.builtin.compile_time import public


@public
def Main() -> bytes:
    return 'NUnLWXALK2G6gYa7RadPLRiQYunZHnncxg '.to_script_hash()


@public
def Main2() -> bytes:
    return '123'.to_script_hash()
