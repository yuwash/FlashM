# cliui.py command-line interface of FlashM 0.1.0
#
# This only works within flashm.py
# see README file for copyright information and version history

# for Python 2
try:
    input = raw_input
except NameError:
    pass

DIALOG_TYPE_OK = 101
DIALOG_TYPE_YES_NO = 102


def prompt(description='', choices=[], default=None):
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


def write(content):
    print(content)


def read(hint='', default=None):
    reply = prompt(hint, ['q! to cancel'], default=default)
    if default is not None and reply == '':
        return default
    elif reply.lower() != 'q!':
        return reply


def read_multiline(hint=''):
    reply = prompt(hint, ['q! to cancel', 'finish with ;;;'])
    if reply.lower() != 'q!':
        while reply[-3:] != ';;;':
            reply += '\n' + input('... ')
        return reply


def dialog(type, hint=None):
    output = ''
    if hint:  # is not None
        output += hint + ' '
    if type == DIALOG_TYPE_OK:
        input(output)
    elif type == DIALOG_TYPE_YES_NO:
        return 'y' == prompt(output, ['(y/n)']).lower()


def choice(options, hint=None, show_options=True):
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
        reply = prompt(output).lower()
        if reply == 'h':
            for key in options:
                print('   ' + '   '.join(options[key]))
            return choice(options, hint, False)
        elif reply in shortcutreturn:
            return shortcutreturn[reply.lower()]
    else:  # if option empty, it just waits for confirmation
        input(output)
