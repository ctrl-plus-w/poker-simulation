from random import shuffle

from src.classes.card import Card

from src.enums.symbol import Symbol

current_id = 1


class Deck:
    default_cards: list[Card] = []
    cards: list[Card] = []

    def __init__(self):
        self.generate_cards()

    def generate_cards(self):
        global current_id
        cards: list[Card] = []

        for value in range(1, 13 + 1):
            for symbol in [Symbol.HEART, Symbol.CLUBS, Symbol.SPADES, Symbol.DIAMONDS]:
                cards.append(Card(current_id, value, symbol))
                current_id += 1

        self.default_cards = cards.copy()
        shuffle(cards)
        self.cards = cards
