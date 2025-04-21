from datetime import datetime, timezone, timedelta
from typing import Optional

from src.classes.sql_statement_builder import SQLInsertStatementBuilder

from src.enums.action import Action

current_id = 1

now = datetime.now(timezone.utc)


def get_now():
    global now
    now += timedelta(0, 0, 0, 0, 1)
    print(now)
    return now


class History:
    id: int = None
    action: Action = None
    value: Optional[int] = None
    round_num: int = None
    created_at: datetime = None

    def __init__(self, action: Action, value: Optional[int], round_num: int):
        self.action = action
        self.value = value
        self.round_num = round_num
        self.created_at = get_now()

        global current_id
        self.id = current_id
        current_id += 1

    def get_sql_statement(self, player: 'Player', game: 'Game'):
        builder = SQLInsertStatementBuilder("history",
                                            ["id", "player_id", "game_id", "action", "value", "round", "created_at"])
        return builder.build([self.id, player.id, game.id, self.action.name, self.value or 'NULL', self.round_num,
                              self.created_at])
