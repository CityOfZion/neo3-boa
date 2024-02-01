if __name__ == '__main__':
    import os
    import sys

    if len(sys.argv) < 2:
        raise ValueError('Missing arguments')

    bumpversion_args = sys.argv[1:]

    here = os.path.abspath(os.path.dirname(__file__))

    if '-h' in bumpversion_args or '--help' in bumpversion_args:
        exit_code = os.system(f'bump-my-version bump --help')
        exit(exit_code)

    exit_code = os.system(f'bump-my-version bump {" ".join(bumpversion_args)} --allow-dirty --no-tag --no-commit')
    if exit_code:
        exit(exit_code)

    exit_code = os.system(f'python {os.sep.join([here, "docs", "make-pdf.py"])}')
    if exit_code:
        exit(exit_code)

    os.system('git checkout boa3')
    os.system('git checkout docs/make-pdf.py')
    os.system('git checkout pyproject.toml')
    os.system('git add .')
    os.system(f'bump-my-version bump {" ".join(bumpversion_args)} --allow-dirty')
