# quiz file handling class for FlashM 0.1.0
# Pau quiz files of Pauker (pauker.sourceforge.net)
#
# This only works within flashm.py
# see README file for copyright information and version history

from . import flashmquiz
import gzip
import os
import xml.dom.minidom

try:
    unicode2 = unicode

    def str(bytes_or_buffer):
        return unicode2(bytes_or_buffer.encode('utf_8'), 'utf_8')
except NameError:
    pass


def load(filename, name):
    pf = gzip.open(filename)

    def sidetext(node):
        return str(
            node.getElementsByTagName('Text').item(0).firstChild.data.strip()
        )
    cards = xml.dom.minidom.parse(pf).getElementsByTagName('Card')
    pf.close()
    cards = []
    for card in cards:
        cards.append([
            sidetext(card.getElementsByTagName('FrontSide').item(0)),
            sidetext(card.getElementsByTagName('ReverseSide').item(0))
        ])
    return flashmquiz.Quiz(name, cards)


def dump(quiz, filename):
    # @param quiz has the type of flashmquiz.Quiz
    pxml = xml.dom.minidom.getDOMImplementation().createDocument(
        None, 'Lesson', None,
    )
    pxml.documentElement.appendChild(
        pxml.createComment(
            'This is a lesson file for Pauker, created by FlashM')
    )
    batchnode = pxml.createElement('Batch')
    for card in quiz.cards:
        cardnode = pxml.createElement('Card')
        for i in (0, 1):
            if i:
                sidenode = pxml.createElement('ReverseSide')
            else:
                sidenode = pxml.createElement('FrontSide')
            textnode = pxml.createElement('Text')
            textnode.appendChild(pxml.createTextNode(card[i].encode('utf_8')))
            sidenode.appendChild(textnode)
            cardnode.appendChild(sidenode)
        batchnode.appendChild(cardnode)
    pxml.documentElement.appendChild(batchnode)
    pf = gzip.open(filename, 'w')
    pxml.writexml(pf, addindent='  ', newl=os.linesep)
    pf.close()
