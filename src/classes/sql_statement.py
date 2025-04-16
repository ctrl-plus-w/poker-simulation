from typing import List

from src.utils import format_sql_value


class SQLStatement:
    def get_sql(self):
        raise Exception("Not implemented")


class SQLTableStatement(SQLStatement):
    def __init__(self, table_name: str):
        self.table_name = table_name


class SQLInsertStatement(SQLTableStatement):
    def __init__(self, table_name: str, columns: List[str], values: List[list]):
        super().__init__(table_name)
        self.columns = columns
        self.values = values

    def get_sql(self):
        columns = ', '.join(self.columns)
        values = ', '.join(map(format_sql_value, self.values))
        return f"INSERT INTO {self.table_name} ({columns}) VALUES ({values});"


class SQLUpdateStatement(SQLTableStatement):
    def __init__(self, table_name: str, set_values: dict, where: str):
        super().__init__(table_name)
        self.set_values = set_values
        self.where = where

    def get_sql(self):
        set_clause = ', '.join([f"{k} = {format_sql_value(v)}" for k, v in self.set_values.items()])
        return f"UPDATE {self.table_name} SET {set_clause} WHERE {self.where};"


class SQLDeleteStatement(SQLTableStatement):
    def __init__(self, table_name: str):
        super().__init__(table_name)

    def get_sql(self):
        return f"DELETE FROM {self.table_name};"


class SQLClearTablesStatement(SQLStatement):
    def get_sql(self):
        return """BEGIN
FOR c IN (SELECT table_name FROM user_tables) LOOP
EXECUTE IMMEDIATE ('DROP TABLE "' || c.table_name || '" CASCADE CONSTRAINTS');
END LOOP;
END;"""
