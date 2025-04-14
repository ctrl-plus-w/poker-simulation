from dataclasses import dataclass

from symbol import Symbol


@dataclass
class Card:
    value: int = None
    symbol: Symbol = None

    @staticmethod
    def stringify_value(value):
        if value == 1:
            return "Ace"
        elif value == 11:
            return "Jack"
        elif value == 12:
            return "Queen"
        elif value == 13:
            return "King"
        else:
            return str(value)

    @staticmethod
    def stringify_symbol(symbol):
        if symbol == Symbol.HEART:
            return "♥"
        elif symbol == Symbol.CLUBS:
            return "♣"
        elif symbol == Symbol.SPADES:
            return "♠"
        elif symbol == Symbol.DIAMONDS:
            return "♦"
        else:
            return str(symbol)

    def __str__(self):
        return f"{self.stringify_value(self.value)} {self.stringify_symbol(self.symbol)}"
