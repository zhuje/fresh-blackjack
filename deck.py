import random
from card import Card
#from group_of_cards import GroupOfCards

class Deck(object):

    def __init__(self, nosd):
        self.nosd = nosd
        self.contents = []
        self.buildDeck()

    def buildDeck(self):
        for d in range (0, self.nosd):
            for i in range (0, 4):
                for j in range (0, 13):
                    new_card = Card(i, j)
                    self.contents.append(new_card)
        self.contents = random.sample(self.contents, len(self.contents))

    def popCard(self):
        try:
            return self.contents.pop()
        except IndexError:
            self.buildDeck()
            return self.popCard()
