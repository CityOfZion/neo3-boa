def deprecated(deprecated_in=None, removed_in=None, current_version=None, details=""):
    if current_version is None:
        import boa3
        current_version = boa3.__version__

    check_module = deprecated_in is None
    details = f'\n{details}'.replace('\n', '\n' + ' ' * 3)

    def wrapper(*args, **kwargs):
        deprecated_version = deprecated_in
        if check_module and len(args) > 0:
            import inspect
            import os.path

            if f'boa3{os.path.sep}builtin' in inspect.getfile(args[0]):
                import boa3
                deprecated_version = boa3.__boa3_builtin_deprecate_version__

        from deprecation import deprecated as deprecated_
        wrap = deprecated_(
            deprecated_in=deprecated_version,
            removed_in=removed_in,
            current_version=current_version,
            details=details
        )
        return wrap(*args, **kwargs)

    return wrapper
