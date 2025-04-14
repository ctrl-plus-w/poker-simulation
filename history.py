from typing import Optional
from dataclasses import dataclass

from action import Action


@dataclass
class History:
    action: Action = None
    value: Optional[int] = None
    round_num: int = None
