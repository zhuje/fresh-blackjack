from card import Card
#from group_of_cards import GroupOfCards

class Hand(object):
    def __init__(self):
        self.outcome = None
        self.contents = []
        self.bet = None

    def getColor(self, i):
        return self.contents[i].color

    def getSuit(self, i):
        return self.contents[i].suit

    def getFaceValue(self, i):
        return self.contents[i].faceValue

    def getNumValue(self, i):
        return self.contents[i].numValue

    def getTotalNumValue(self):
        totalNumValue = 0
        for i in range(0, len(self.contents)):
            totalNumValue += self.contents[i].numValue
        return totalNumValue

    def getInfo(self, i):
        return f"{self.contents[i].faceValue} of {self.contents[i].suit}"

    def getAllInfo(self, i):
        return f"{self.contents[i].color} {self.contents[i].faceValue} of {self.contents[i].suit}"

    def switchAce(self):
        for i in range(0, len(self.contents)):
            if self.contents[i].numValue == 11 and self.getTotalNumValue() > 21:
                self.contents[i].switchAceValue()
            else:
                pass

    def add(self, new_card):
            self.contents.append(new_card)

    def popCard(self):
        return self.contents.pop()
