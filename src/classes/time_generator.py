from datetime import datetime, timedelta, timezone
from random import uniform


class ProgressiveTimeGenerator:
    def __init__(self):
        self.last_time = datetime.now(timezone.utc)

    def now(self):
        increment_seconds = uniform(0.1, 30)
        self.last_time += timedelta(seconds=increment_seconds)

        return self.last_time


time_generator = ProgressiveTimeGenerator()
