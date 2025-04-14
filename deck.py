from typing import List
from random import shuffle

from symbol import Symbol
from card import Card


class Deck:
    cards: List[Card] = []

    def __init__(self):
        self.generate_cards()

    def generate_cards(self):
        cards: List[Card] = []

        for value in range(1, 13 + 1):
            for symbol in [Symbol.HEART, Symbol.CLUBS, Symbol.SPADES, Symbol.DIAMONDS]:
                cards.append(Card(value, symbol))

        shuffle(cards)
        self.cards = cards
