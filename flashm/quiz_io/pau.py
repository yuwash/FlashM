# quiz file handling class for FlashM 0.1.0
# Pau quiz files of Pauker (pauker.sourceforge.net)
#
# This only works within flashm.py
# see README file for copyright information and version history

from .base import QuizIO, XMLQuizIOMixin
import gzip
import os

try:
    unicode2 = unicode

    def str(bytes_or_buffer):
        return unicode2(bytes_or_buffer.encode('utf_8'), 'utf_8')
except NameError:
    pass


class PaukerQuizIO(XMLQuizIOMixin, QuizIO):
    xml_cards_root_tag = 'Card'
    xml_cards_question_tag = 'FrontSide'
    xml_cards_answer_tag = 'ReverseSide'
    out_xml_root_tag = 'Lesson'
    out_xml_pattern = [('Batch', [
        ('Card', [
            ('FrontSide', [('Text', '{question}')]),
            ('ReverseSide', [('Text', '{answer}')]),
        ]),
    ])]
    out_xml_comment = 'This is a lesson file for Pauker, created by FlashM'

    @staticmethod
    def get_sidetext(node):
        return str(
            node.getElementsByTagName('Text').item(0).firstChild.data.strip()
        )

    @classmethod
    def load(cls, filename, name):
        with gzip.open(filename) as pf:
            return cls.build_quiz_from_file(pf, name)

    @classmethod
    def dump(cls, quiz, filename):
        pxml = cls.build_xml(quiz)
        with gzip.open(filename, 'w') as pf:
            pxml.writexml(pf, addindent='  ', newl=os.linesep)
