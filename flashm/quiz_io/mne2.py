from .base import ZippedXMLQuizIO


class Mnemosyne2QuizIO(ZippedXMLQuizIO):
    xml_cards_question_tag = 'f'
    xml_cards_answer_tag = 'b'
    out_xml_root_tag = 'openSM2sync'
    out_xml_pattern = [
        ('log', [('name', '{name}')]),
        [('log', [('b', '{answer}'), ('f', '{question}')])],
    ]
    out_xml_comment = 'This is a quiz file for Mnemosyne 2, created by FlashM'
    xmlfile_path = 'cards.xml'
    out_xmlfile_pattern = xmlfile_path

    @classmethod
    def get_cards_root(cls, xmldoc):
        def check(node):
            # some log[type="16"] elements contain m_1, p_1 elements
            # instead of b elements;
            # those are not supported at the moment
            return bool(node.getElementsByTagName(cls.xml_cards_answer_tag))
        return [
            node for node in xmldoc.getElementsByTagName('log')
            if node.getAttribute('type') == '16' and check(node)]
