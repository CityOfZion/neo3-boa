def list_inner_packages(rootdir: str) -> list:
    import os.path

    inner_dirs = []

    if os.path.isdir(rootdir):
        rootdir = os.path.abspath(rootdir)
        for file in os.listdir(rootdir):
            dir_ = os.path.join(rootdir, file)

            if os.path.isdir(dir_):
                inner_dirs.extend(list_inner_packages(dir_))
                if os.path.isfile(os.path.join(dir_, '__init__.py')):
                    inner_dirs.append(dir_)

    return inner_dirs
