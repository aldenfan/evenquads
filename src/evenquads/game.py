
from dataclasses import dataclass
import random
import itertools

DEBUG = False

# Any 4 unique numbers for each attribute
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
        if isinstance(other, Card):
            return self.id < other.id
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.id == other.id
        return NotImplemented

    def __repr__(self) -> str:
        return f"{self.id}"

class Pile(list):

    def __init__(self):
        super().__init__()

    @property
    def size(self):
        return len(self)
    
    def shuffle(self):
        random.shuffle(self)

class Deck(Pile):

    def __init__(self):
        super().__init__()
        #self.cards = []
        for color in colors:
            for shape in shapes:
                for count in counts:
                    card = Card(color=color, shape=shape, count=count)
                    # self.cards.append(card)
                    self.append(card)



class Game:

    def __init__(self):

        self.deck = Deck()
        self.deck.shuffle()

        self.pool = Pile()
        self.is_perfect = False

    def play(self):
        """
        Play a single round:
        1. Top up pool with 8 cards. Make sure to pop from top of deck.
        2. Look for sets. Randomize order of looking?
        3. If set is found, remove from pool.
        4. Repeat until end of deck.
        """

        if DEBUG:
            print(f"Initial deck:")
            print(self.deck)
        
        while self.deck.size > 0 or self.pool.size > 0:

            # Refill central card pool
            while self.pool.size < 8 and self.deck.size > 0:
                self.pool.append(self.deck.pop())

            # Check if pool has a quad
            has_quad, quad = check_pool(self.pool)

            # If there's no quad, add cards to pool until there is
            while not has_quad and self.deck.size > 0:
                if DEBUG:
                    print(f"No quad. Adding a card -> {self.pool.size}")
                self.pool.append(self.deck.pop())
                has_quad, quad = check_pool(self.pool)

            # Remove quad from pool
            if has_quad:
                for card in quad:
                    self.pool.remove(card)  

            if DEBUG:
                print(f"End of round. {self.deck.size} {self.pool.size}")

            # End conditions
            if self.deck.size == 0 and self.pool.size > 0 and not has_quad:
                self.is_perfect = False
                if DEBUG:
                    print(f"End of game. Non-perfect.")
                break
            if self.deck.size == 0 and self.pool.size == 0:
                self.is_perfect = True
                if DEBUG:
                    print(f"End of game. perfect.")
                break
            # input()
    
        # print(self.deck)
        # print(len(self.pool))
        return self.is_perfect

def check_pool(pool):

    pool.shuffle()

    # Cycle through all combinations of cards and look for a quad
    for combo in itertools.combinations(pool, 4):
        
        if is_quad(combo):
            if DEBUG:
                print(f"Found quad!")
                print(combo)
            return True, combo

    return False, []

def is_quad(combo):

    colors = [ c.color for c in combo ]
    shapes = [ c.shape for c in combo ]
    counts = [ c.count for c in combo ]
    
    return attr_is_quad(colors) and attr_is_quad(shapes) and attr_is_quad(counts)
        

def attr_is_quad(attrs):

    """
    One of:
    - each attribute is the same
    - each attribute is unique
    - there are two pairs of attributes
    """

    unique_attrs = set(attrs)

    def is_all_same():
        return (len(unique_attrs) == 1)
    def is_all_diff():
        return (len(unique_attrs) == len(attrs))
    def is_pairs():
        first_attr = list(unique_attrs)[0]
        return (len(unique_attrs) == 2) & (attrs.count(first_attr) == 2)

    return is_all_same() | is_all_diff() | is_pairs()


if __name__ == '__main__':


    n_games = 10000
    n_perfect_games = 0
    for n in range(n_games):
        if n%1000 == 0:
            print(f"Simulating {n}/{n_games}")

        game = Game()
        is_perfect = game.play()
        
        n_perfect_games += int(is_perfect)

    print(f"# of perfect games: {n_perfect_games}/{n_games}")
