#! /usr/bin/env python

from argparse import ArgumentParser
from .ui import Session, NOTICE


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
        from .cliui import CliUi
        ui = CliUi()
    elif args.interaction == 'fullterm':
        from .fulltermui import FullTerminalUi
        ui = FullTerminalUi()
    # open_quiz_file returns False if user wants
    # to quit without opening or creating any quiz ('q!')
    session = Session.open_quiz_file(uimodule=ui, quiet=args.quiet)
    if session:
        session.start()


if __name__ == "__main__":
    main()
