#
# Copyright (c) 2008, 2009 Adam Marshall Smith
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
import os, pickle

class CardStore(object):
    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(filename):
            self.cards = pickle.load(file(filename, 'r+b'))
        else:
            self.cards = {}
    
    def save(self):
        pickle.dump(self.cards, file(self.filename, 'w+b'))
    
    def getCard(self, key, partialKeys=None):
        card = self.cards.get(key,{'key':key})
        if partialKeys is None:
            return card
        else:
            return dict([(k, card.get(k,None)) for k in partialKeys])
    
    def setCard(self, key, card):
        self.cards[key] = card
        self.save()
        
    def updateCard(self, key, partialCard):
        card = self.getCard(key)
        card.update(partialCard)
        self.setCard(key, card)

    def hasCard(self, key):
        return self.cards.has_key(key)
