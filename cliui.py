# cliui.py command-line interface of FlashM 0.1.0
#
# This only works within flashm.py
# see README file for copyright information and version history

DIALOG_TYPE_OK = 101
DIALOG_TYPE_YES_NO = 102

def write(content):
    print content

def read(hint = '', default = None):
    if default != None:
        defhint = 'default: %s; ' %default
    else:
        defhint = ''
    input = raw_input(hint +' (' +defhint +'q! to cancel) -> ')
    if default != None and input == '':
        return default
    elif input.lower() != 'q!':
        return input

def read_multiline(hint = ''):
    input = raw_input(hint +' (q! to cancel, finish with ;;;) -> ')
    if input.lower() != 'q!':
        while input[-3:]!=';;;':
            input += '\n' +raw_input('... ')
        return input

def dialog(type, hint = None):
    output = ''
    if hint: #is not None
        output += hint +' '
    if type == DIALOG_TYPE_OK:
        raw_input(output)
    elif type == DIALOG_TYPE_YES_NO:
        return 'y' == raw_input(output +'(y/n) -> ').lower()

def choice(options, hint = None, show_options = True):
    #@param options:
    #    dictionary of
    #    option value to return => (shortcut, [description])
    #
    output = ''
    if hint: #is not None
        output += hint +' '
    if options: #is not empty
        shortcutreturn = {}
        for key in options:
            shortcutreturn[options[key][0].lower()] = key
        if show_options:
            optionnotes = []
            for key in options:
                optionnotes.append(': '.join(options[key])) 
            output += '(' +'/'.join(optionnotes) +') '
        else:
            helpcommand = 'h'
            while helpcommand in shortcutreturn:
                helpcommand += 'h'
            output += '(%s for help) ' %helpcommand
        input = raw_input(output +'-> ').lower()
        if input == 'h':
            for key in options:
                print('   ' +'   '.join(options[key]))
            return choice(options, hint, False)
        elif input in shortcutreturn:
            return shortcutreturn[input.lower()]
    else: #if option empty, it just waits for confirmation
        raw_input(output)
