from datetime import datetime, timezone
from typing import Optional

from src.utils import get_apex_datetime

from src.enums.action import Action

current_id = 1


class History:
    id: int = None
    action: Action = None
    value: Optional[int] = None
    round_num: int = None
    created_at: datetime = datetime.now(timezone.utc)

    def __init__(self, action: Action, value: Optional[int], round_num: int):
        self.action = action
        self.value = value
        self.round_num = round_num

        global current_id
        self.id = current_id
        current_id += 1

    def get_sql(self, player: 'Player', game: 'Game'):
        return f"INSERT INTO history (id, player_id, game_id, action, value, round, created_at) VALUES ({self.id}, {player.id}, {game.id}, '{self.action.name}', {self.value or 'NULL'}, {self.round_num}, {get_apex_datetime(self.created_at)});"
