class Card(object):

    possibleSuits = ['Clubs', 'Spades', 'Diamonds', 'Hearts']

    possibleColors = {'Clubs': 'black', 'Spades': 'black', 'Diamonds': 'red', 'Hearts': 'red'}

    possibleValues = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, suit, value):
        self.suit = self.possibleSuits[suit]
        self.color = self.possibleColors[self.suit]
        self.faceValue = self.possibleValues[value]
        self.numValue = None
        self.createNumValue()

    def createNumValue(self):
        if self.faceValue == 'Ace':
            self.numValue = 11
        elif any(self.faceValue == x for x in ['Jack', 'Queen', 'King']):
            self.numValue = 10
        else:
            self.numValue = self.faceValue
        #return self.numValue

    def switchAceValue(self):
        self.numValue = 1

    def info(self):
        return f"{self.faceValue} of {self.suit}"

    def allInfo(self):
        return f"{self.color} {self.faceValue} of {self.suit}"
