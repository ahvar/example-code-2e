import collections


"""
Although FrenchDeck implicitly inherits from the object class, most of its functionality
is not inherited, but comes from leveraging the data model and composition.
"""
Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        """
        Just by implementing __getitem__(), our deck is iterable
        If collection has no __contains__(), the [] operator does
        a sequential scan
        """
        return self._cards[position]


suit_values = dict(spades=3,hearts=2,diamonds=1,clubs=0)
def spades_high(card):
        """
        a common system of ranking is by rank (with aces being highest),
        then by suit in the order of spaces -> hearts -> diamonds -> clubs
        """
        rank_value = FrenchDeck.ranks.index(card.rank)
        return rank_value * len(suit_values) + suit_values[card.suit]
  

if __name__ == "__main__":
     french_deck = FrenchDeck()
     for card in sorted(french_deck, key=spades_high):
          print(card)
    
    
