from dataclasses import dataclass
from datetime import datetime, timezone

from src.utils import get_apex_datetime

from src.enums.symbol import Symbol


@dataclass
class Card:
    id: int = None
    value: int = None
    symbol: Symbol = None
    created_at: datetime = datetime.now(timezone.utc)

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

    def get_sql(self, game: "Game"):
        return f"INSERT INTO deck_card (id, value, symbol, game_id, created_at) VALUES ({self.id}, {self.value}, '{self.symbol.value}', {game.id}, {get_apex_datetime(self.created_at)});"

    def __str__(self):
        return f"{self.stringify_value(self.value)} {self.stringify_symbol(self.symbol)}"
