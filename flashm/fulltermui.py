# fulltermui.py full screen terminal interface of FlashM
#
# This only works within flashm.py
# see README file for copyright information and version history

from __future__ import unicode_literals

import asyncio
from tempfile import NamedTemporaryFile
import time
import subprocess
from prompt_toolkit.shortcuts import dialogs
from .ui import Ui, ReadCancelError, StopPlayback

EDITOR = 'vim'


class PlaybackDialogNotRunningError(RuntimeError):
    pass


class FullTerminalUi(Ui):
    _playback_app = None

    def prompt(self, description='', choices=[], default=None):
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
        return dialogs.input_dialog(**dialog_kwargs).run()

    def write(self, content):
        dialogs.message_dialog(text=content).run()

    async def playback_show_card(self, card, duration):
        if self._playback_app is None or not self._playback_app.is_running:
            raise StopPlayback()  # probably dialog was closed
        label = get_dialog_body(self._playback_app.layout.container)
        label.text = self._card_repr(card)
        self._playback_app.invalidate()
        await asyncio.sleep(duration)

    async def playback_async(self, quiz):
        try:
            while not self._playback_app.is_running:
                await asyncio.sleep(0.1)
            await super(FullTerminalUi, self).playback_async(quiz)
        except PlaybackDialogNotRunningError:
            pass  # probably dialog was closed
        finally:
            if self._playback_app.is_running:
                self._playback_app.exit()

    def playback(self, quiz):
        self._playback_app = dialogs.message_dialog(
            title='Playback', text='…')
        self._playback_app.create_background_task(self.playback_async(quiz))
        self._playback_app.run()

    def read(self, hint='', default=None):
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
        reply = dialogs.input_dialog(text=text).run()
        if reply:
            return reply
        elif reply is None:
            raise ReadCancelError
        else:
            return default

    def read_multiline(self, hint=''):
        self.write(hint)
        with NamedTemporaryFile(mode='r') as replyfile:
            ret = subprocess.call([EDITOR, replyfile.name])
            reply = replyfile.read()
            if ret != 0:
                self.write('discarding input:\n' + reply)
                return False
            return reply

    def yes_no_dialog(self, hint=None):
        return dialogs.yes_no_dialog(text=hint).run()

    def choice(self, options, hint=None, show_options=True):
        if not show_options:
            NotImplementedError('options are always shown!')
        reply = dialogs.radiolist_dialog(text=hint, values=[(
            key,
            value[0] + (' ' + value[1] if len(value) > 1 else ''),
        ) for key, value in options.items()]).run()
        return reply


def get_box_body(box):
    return box.children[1].children[1]


def get_frame_body(frame):
    return frame.children[-2].children[1]


def get_dialog_body(dialog_pt_container):
    # Box -> Shadow -> Frame -> DynamicContainer -> HSplit -> Box -> DynamicContainer
    return get_box_body(
        get_frame_body(get_box_body(dialog_pt_container).content)
        .get_container().children[0]
    ).get_container()
