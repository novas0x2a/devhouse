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