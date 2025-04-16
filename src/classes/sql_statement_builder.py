from typing import List

from src.classes.sql_statement import SQLInsertStatement


class SQLStatementBuilder:
    def build(self):
        raise Exception("Not implemented")


class SQLTableStatementBuilder(SQLStatementBuilder):
    def __init__(self, table_name: str):
        self.table_name = table_name


class SQLInsertStatementBuilder:
    def __init__(self, table_name: str, columns: List[str]):
        self.table_name = table_name
        self.columns = columns

    def build(self, values: List):
        return SQLInsertStatement(self.table_name, self.columns, values)
