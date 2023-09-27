if __name__ == '__main__':
    import os
    import sys

    if len(sys.argv) < 2:
        raise ValueError('Missing arguments')

    bump2version_args = sys.argv[1:]

    here = os.path.abspath(os.path.dirname(__file__))
    config_file = os.path.sep.join([here, 'docs', '.bumpversion.cfg'])

    if '-h' in bump2version_args or '--help' in bump2version_args:
        exit_code = os.system(f'bump2version {" ".join(bump2version_args)}')
        exit(exit_code)

    exit_code = os.system(f'bump2version {" ".join(bump2version_args)} --config-file {config_file} --allow-dirty')
    if exit_code:
        exit(exit_code)

    exit_code = os.system(f'python {os.sep.join([here, "docs", "make-pdf.py"])}')
    if exit_code:
        exit(exit_code)

    os.system('git checkout boa3')
    os.system('git add .')
    os.system(f'bump2version {" ".join(bump2version_args)} --allow-dirty')
