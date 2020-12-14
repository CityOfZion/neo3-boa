from boa3.builtin import public


@public
def bytes_to_bool(args: bytes) -> bool:
    return args.to_bool()
