# quiz file handling class for FlashM 0.1.0
# Pau quiz files of Pauker (pauker.sourceforge.net)
#
# This only works within flashm.py
# see README file for copyright information and version history

import flashmquiz, gzip, os, xml.dom.minidom

def load(filename, name):
    pf = gzip.open(filename)
    sidetext = (lambda node:
        unicode(node.getElementsByTagName('Text').item(0).firstChild.data.strip().encode('utf_8'), 'utf_8')
    )
    cards = xml.dom.minidom.parse(pf).getElementsByTagName('Card')
    pf.close()
    set = []
    for card in cards:
        set.append([
            sidetext(card.getElementsByTagName('FrontSide').item(0)),
            sidetext(card.getElementsByTagName('ReverseSide').item(0))
        ])
    return flashmquiz.quiz(name, set)
    
def dump(quiz, filename):
    #@param quiz has the type of flashmquiz.quiz
    pxml = xml.dom.minidom.getDOMImplementation().createDocument(None, 'Lesson', None)
    pxml.documentElement.appendChild(
        pxml.createComment('This is a lesson file for Pauker, created by FlashM')
    )
    batchnode = pxml.createElement('Batch')
    for card in quiz.set:
        cardnode = pxml.createElement('Card')
        for i in (0,1):
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
    pxml.writexml(pf, addindent = '  ', newl = os.linesep)
    pf.close()
