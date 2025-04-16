from typing import List
from random import shuffle

from symbol import Symbol
from card import Card

current_id = 1


class Deck:
    default_cards: List[Card] = []
    cards: List[Card] = []

    def __init__(self):
        self.generate_cards()

    def generate_cards(self):
        global current_id
        cards: List[Card] = []

        for value in range(1, 13 + 1):
            for symbol in [Symbol.HEART, Symbol.CLUBS, Symbol.SPADES, Symbol.DIAMONDS]:
                cards.append(Card(current_id, value, symbol))
                current_id += 1

        self.default_cards = cards.copy()
        shuffle(cards)
        self.cards = cards
