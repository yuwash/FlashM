# cliui.py command-line interface of FlashM 0.1.0
#
# This only works within flashm.py
# see README file for copyright information and version history

import asyncio
from .ui import Ui, StopPlayback

# for Python 2
try:
    input = raw_input
except NameError:
    pass


class CliUi(Ui):
    def prompt(self, description='', choices=[], default=None):
        if choices or default:
            if default:
                defhint = 'default: ' + default
                if choices:
                    defhint += '; '
            else:
                defhint = ''
            hint = '(' + defhint + ', '.join(choices) + ')'
            help_text = ' '.join([description, hint])
        else:
            help_text = description
        return input(' '.join([help_text, '-> ']))

    def write(self, content):
        print(content)

    async def playback_show_card(self, card, duration):
        try:
            self.show_card(card)
            await asyncio.sleep(duration)
        except KeyboardInterrupt:
            raise StopPlayback()

    def read_multiline(self, hint=''):
        reply = self.prompt(hint, ['q! to cancel', 'finish with ;;;'])
        if reply.lower() != 'q!':
            while reply[-3:] != ';;;':
                reply += '\n' + input('... ')
            return reply

    def yes_no_dialog(self, hint=None):
        return 'y' == self.prompt(hint, ['y/n']).lower()

    def choice(self, options, hint=None, show_options=True):
        # @param options:
        #    dictionary of
        #    option value to return => (shortcut, [description])
        #
        output = ''
        if hint:  # is not None
            output += hint + ' '
        if options:  # is not empty
            shortcutreturn = {}
            for key in options:
                shortcutreturn[options[key][0].lower()] = key
            if show_options:
                optionnotes = []
                for key in options:
                    optionnotes.append(': '.join(options[key]))
                output += '(' + '/'.join(optionnotes) + ') '
            else:
                helpcommand = 'h'
                while helpcommand in shortcutreturn:
                    helpcommand += 'h'
                output += '(%s for help) ' % helpcommand
            reply = self.prompt(output).lower()
            if reply == 'h':
                for key in options:
                    print('   ' + '   '.join(options[key]))
                return self.choice(options, hint, False)
            elif reply in shortcutreturn:
                return shortcutreturn[reply.lower()]
        else:  # if option empty, it just waits for confirmation
            input(output)
