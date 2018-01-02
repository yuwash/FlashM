#! /usr/bin/env python

from argparse import ArgumentParser
from flashm import Session, NOTICE


def main():
    argparser = ArgumentParser(description=NOTICE)
    argparser.add_argument(
        '-q', '--quiet', action='store_true',
        help='turn off verbose output',
    )
    argparser.add_argument(
        '-i', '--interaction', choices=['cli', 'fullterm'], nargs='?',
        const='cli', default='cli',
        help='UI for interaction',
    )
    args = argparser.parse_args()
    if args.interaction == 'cli':
        from cliui import CliUi
        ui = CliUi()
    elif args.interaction == 'fullterm':
        from fulltermui import FullTerminalUi
        ui = FullTerminalUi()
    Session.open_quiz_file(uimodule=ui, quiet=args.quiet).start()


if __name__ == "__main__":
    main()
