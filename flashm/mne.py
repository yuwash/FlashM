# mne.py quiz file handling class for FlashM 0.1.0
# quiz files of Mnemosyne (mnemosyne.org)
#
# This only works within flashm.py
# see README file for copyright information and version history

from . import flashmquiz
import zipfile
import os
import xml.dom.minidom

try:
    unicode2 = unicode

    def str(bytes_or_buffer):
        return unicode2(bytes_or_buffer.encode('utf_8'), 'utf_8')
except NameError:
    pass


def load(filename, name):
    zf = zipfile.ZipFile(filename)
    xmlfilename = zf.namelist()[0]

    def sidetext(node):
        return str(node.firstChild.data.strip())
    cards = (
        xml.dom.minidom.parse(zf.open(xmlfilename))
        .getElementsByTagName('item')
    )
    zf.close()
    set = []
    for card in cards:
        set.append([
            sidetext(card.getElementsByTagName('Q').item(0)),
            sidetext(card.getElementsByTagName('A').item(0))
        ])
    return flashmquiz.Quiz(name, set)


def dump(quiz, filename):
    # @param quiz has the type of flashmquiz.Quiz
    mxml = xml.dom.minidom.getDOMImplementation().createDocument(
        None, 'mnemosyne', None,
    )
    mxml.documentElement.appendChild(
        mxml.createComment(
            'This is a quiz file for Mnemosyne, created by FlashM'
        )
    )
    catnode = mxml.createElement('category')
    namenode = mxml.createElement('name')
    namenode.appendChild(mxml.createTextNode(quiz.name))
    catnode.appendChild(namenode)
    mxml.documentElement.appendChild(catnode)
    for card in quiz.set:
        itemnode = mxml.createElement('item')
        for i in (0, 1):
            if i:  # == 1
                sidenode = mxml.createElement('A')
            else:  # i == 0
                sidenode = mxml.createElement('Q')
            sidenode.appendChild(mxml.createTextNode(card[i].encode('utf_8')))
            itemnode.appendChild(sidenode)
        mxml.documentElement.appendChild(itemnode)
    mfname = quiz.name + '.XML'
    mf = open(mfname, 'w')
    mxml.writexml(mf, addindent='  ', newl=os.linesep)
    mf.close()
    zf = zipfile.ZipFile(filename, 'w')
    zf.write(mfname)
    zf.close()
    os.remove(mfname)
