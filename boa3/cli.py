from argparse import ArgumentParser, RawDescriptionHelpFormatter

from boa3.internal import constants
from boa3.internal.cli_commands import commands


def main():
    n3boa = ArgumentParser(description=f"neo3-boa by COZ - version {constants.BOA_VERSION}"
                                       "\nWrite smart contracts for Neo3 in Python",
                           formatter_class=RawDescriptionHelpFormatter,
                           )
    n3boa.add_argument("-v", "--version", action="version",
                       version=f"neo3-boa {constants.BOA_VERSION}")

    n3_subparser = n3boa.add_subparsers(title='Commands')

    # Initialize all commands on cli_commands
    for command in commands:
        command(n3_subparser).add_arguments_and_callback()

    # read command line and get the correct command requested
    args = n3boa.parse_args()

    # execute subparser commands
    if hasattr(args, 'func'):
        args.func(vars(args))
    else:
        import sys
        n3boa.print_help(sys.stderr)


if __name__ == "__main__":
    main()
