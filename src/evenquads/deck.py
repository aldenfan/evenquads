from dataclasses import dataclass
import random

colors = [1,2,3,4]
shapes = [1,2,3,4]
counts = [1,2,3,4]

@dataclass
class Card:

    color: int
    shape: int 
    count: int

    @property
    def id(self):
        return 100*self.color + 10*self.shape + self.count 

    def __lt__(self, other):
        return self.id < other.id 


class Deck:

    def __init__(self):

        self.cards = []
        for color in colors:
            for shape in shapes:
                for count in counts:
                    card = Card(color=color, shape=shape, count=count)
                    self.cards.append(card)

    @property
    def size(self):
        return len(self.cards)
    
    def shuffle(self):
        random.shuffle(self.cards)

    def pop(self):
        return self.cards.pop()

    def __repr__(self) -> str:
        return f"{[card.id for card in self.cards]}"
    
        

if __name__ == '__main__':

    card1 = Card(color=1, shape=2, count=3)
    card2 = Card(color=1, shape=2, count=2)

    cards = [card1, card2]

    print(card1, card1.id)
    print(card2, card2.id)
    print(card1 < card2)
    print(sorted(cards))

    deck = Deck()
    print(deck.size)
    deck.shuffle()
    print([c.id for c in deck.cards])
