from typing import List

from src.utils import format_sql_value


class SQLStatement:
    def get_sql(self):
        raise Exception("Not implemented")


class SQLInsertStatementBuilder:
    def __init__(self, table_name: str, columns: List[str]):
        self.table_name = table_name
        self.columns = columns

    def build(self, values: List):
        return SQLInsertStatement(self.table_name, self.columns, values)


class SQLInsertStatement(SQLStatement):
    def __init__(self, table_name: str, columns: List[str], values: List[list]):
        self.table_name = table_name
        self.columns = columns
        self.values = values

    def get_sql(self):
        columns = ', '.join(self.columns)
        values = ', '.join(map(format_sql_value, self.values))
        return f"INSERT INTO {self.table_name} ({columns}) VALUES ({values});"


class SQLUpdateStatement(SQLStatement):
    def __init__(self, table_name: str, set_values: dict, where: str):
        self.table_name = table_name
        self.set_values = set_values
        self.where = where

    def get_sql(self):
        set_clause = ', '.join([f"{k} = {format_sql_value(v)}" for k, v in self.set_values.items()])
        return f"UPDATE {self.table_name} SET {set_clause} WHERE {self.where};"


class SQLDeleteStatement(SQLStatement):
    def __init__(self, table_name: str):
        self.table_name = table_name

    def get_sql(self):
        return f"DELETE FROM {self.table_name};"
