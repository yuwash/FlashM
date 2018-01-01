# fulltermui.py full screen terminal interface of FlashM
#
# This only works within flashm.py
# see README file for copyright information and version history

from __future__ import unicode_literals

from tempfile import NamedTemporaryFile
import subprocess
from prompt_toolkit.shortcuts import dialogs
from cliui import DIALOG_TYPE_OK, DIALOG_TYPE_YES_NO

EDITOR = 'vim'


def prompt(description='', choices=[], default=None):
    dialog_kwargs = {'title': description}
    choiceshint = ', '.join(choices)
    if default:
        text = 'default: ' + default
        if choices:
            text += '; ' + choiceshint
    else:
        text = choiceshint
    if text:
        dialog_kwargs['text'] = text
    return dialogs.input_dialog(**dialog_kwargs)


def write(content):
    dialogs.message_dialog(text=content)


def read(hint='', default=None):
    if hint:
        text = hint
    else:
        text = ''
    if default is not None:
        defaulthint = '(default: {})'.format(default)
        if hint:
            text += '; ' + defaulthint
        else:
            text = defaulthint
    reply = dialogs.input_dialog(text=text)
    if reply is None:
        return default
    else:
        return reply


def read_multiline(hint=''):
    write(hint)
    with NamedTemporaryFile(mode='r') as replyfile:
        ret = subprocess.call([EDITOR, replyfile.name])
        reply = replyfile.read()
        if ret != 0:
            write('discarding input:\n' + reply)
            return False
        return reply


def dialog(type, hint=None):
    if type == DIALOG_TYPE_OK:
        write(hint)
    elif type == DIALOG_TYPE_YES_NO:
        return dialogs.yes_no_dialog(text=hint)


def choice(options, hint=None, show_options=True):
    if not show_options:
        NotImplementedError('options are always shown!')
    reply = dialogs.radiolist_dialog(text=hint, values=[(
        key,
        value[0] + (' ' + value[1] if len(value) > 1 else ''),
    ) for key, value in options.items()])
    return reply
