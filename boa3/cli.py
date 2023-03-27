from argparse import ArgumentParser

from boa3.cli_commands import commands


def main():
    n3boa = ArgumentParser()

    n3_subparser = n3boa.add_subparsers(title='Commands')

    # Initialize all commands on cli_commands
    for command in commands:
        command(n3_subparser).add_arguments_and_callback()

    # read command line and get the correct command requested
    args = n3boa.parse_args()

    # execute command
    if hasattr(args, 'func'):
        args.func(vars(args))


if __name__ == "__main__":
    main()
