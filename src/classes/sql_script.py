from typing import List, Optional

from src.classes.sql_statement import SQLStatement


class SQLScript:
    statements: List[SQLStatement]

    def __init__(self, statements: list[SQLStatement] = None):
        self.statements = statements or []

    def add(self, statement: SQLStatement):
        self.statements.append(statement)

    def merge(self, *others: 'SQLScript'):
        for other in others:
            self.statements.extend(other.statements)

    def get_sql(self):
        return '\n'.join([s.get_sql() for s in self.statements])
