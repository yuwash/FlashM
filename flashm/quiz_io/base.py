import os
import tempfile
import xml.dom.minidom
import zipfile

from ..flashmquiz import Quiz

try:
    unicode2 = unicode

    def str(bytes_or_buffer):
        return unicode2(bytes_or_buffer.encode('utf_8'), 'utf_8')
except NameError:
    pass


class QuizIO(object):
    @staticmethod
    def load(filename, name):
        """
        :param str filename: path to the file to read from
        :param str name: name of the quiz to load
        """
        raise NotImplementedError('please implement in a subclass!')

    @staticmethod
    def dump(quiz, filename):
        """
        :param flashmquiz.Quiz cards: the content to dump
        :param str filename: path to the file to write to
        """
        raise NotImplementedError('please implement in a subclass!')


class XMLQuizIOMixin(object):
    xml_cards_root_tag = 'item'
    xml_cards_question_tag = 'Q'
    xml_cards_answer_tag = 'A'
    out_xml_root_tag = 'mnemosyne'
    out_xml_pattern = [
        ('category', [('name', '{name}')]),
        [('item', [('Q', '{question}'), ('A', '{answer}')])],
    ]
    out_xml_comment = 'This is a quiz file for Mnemosyne, created by FlashM'

    @staticmethod
    def get_sidetext(node):
        return str(node.firstChild.data.strip())

    @classmethod
    def build_quiz_from_file(cls, readable, name):
        cards_root = xml.dom.minidom.parse(readable).getElementsByTagName(
            cls.xml_cards_root_tag)
        cards = [[
            cls.get_sidetext(card_node.getElementsByTagName(tag_name).item(0))
            for tag_name in (
                cls.xml_cards_question_tag, cls.xml_cards_answer_tag,
            )] for card_node in cards_root]
        return Quiz(name, cards)

    @classmethod
    def _build_xml_children(
            cls, pattern, xmldoc, node, quiz, card=None, context=None):
        if isinstance(pattern, list):
            for card in quiz.cards:
                cls._build_xml_children(
                    pattern[0], xmldoc, node, quiz, card, context)
        elif isinstance(pattern, tuple):
            tag_name, children_pattern = pattern
            child_node = xmldoc.createElement(tag_name)
            node.appendChild(child_node)
            if isinstance(children_pattern, list):
                for child_pattern in children_pattern:
                    cls._build_xml_children(
                        child_pattern, xmldoc, child_node, quiz, card, context)
            else:  # actually one child that is a text node
                cls._build_xml_children(
                    children_pattern, xmldoc, child_node, quiz, card, context)
        else:
            if context is None:
                context = {}
            if card is not None:
                context.update(zip(('question', 'answer'), card))
            text = pattern.format(**context)
            child_node = xmldoc.createTextNode(text.encode('utf_8'))
            node.appendChild(child_node)

    @classmethod
    def build_xml(cls, quiz):
        xmldoc = xml.dom.minidom.getDOMImplementation().createDocument(
            None, cls.out_xml_root_tag, None,
        )
        xmldoc.documentElement.appendChild(
            xmldoc.createComment(cls.out_xml_comment))
        context = {'name': quiz.name}
        for pattern_item in cls.out_xmlfile_pattern:
            cls.build_xml(
                pattern_item, xmldoc, xmldoc.documentElement, quiz,
                context=context)
        return xmldoc


class ZippedXMLQuizIO(XMLQuizIOMixin, QuizIO):
    xmlfile_path = ''  # empty means there is only one file in the zip
    out_xmlfile_pattern = '{name}.XML'

    @classmethod
    def load(cls, filename, name):
        with zipfile.ZipFile(filename) as zf:
            xmlfile_path = cls.xmlfile_path or zf.namelist()[0]
            with zf.open(xmlfile_path) as xmlf:
                return cls.build_quiz_from_file(xmlf, name)

    @classmethod
    def dump(cls, quiz, filename):
        mxml = cls.build_xml(quiz)
        mfname = cls.out_xmlfile_pattern.format(name=quiz.name)
        with tempfile.NamedTemporaryFile() as mf:
            mxml.writexml(mf, addindent='  ', newl=os.linesep)
            with zipfile.ZipFile(filename, 'w') as zf:
                zf.write(mf.name, arcname=mfname)
