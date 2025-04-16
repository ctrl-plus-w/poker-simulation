from datetime import datetime


def get_apex_datetime(date: datetime):
    str_date = date.strftime('%d-%b-%y %I.%M.%S.%f %p %z')
    return f"'{str_date[:-2]}:{str_date[-2:]}'".upper()


def format_sql_value(value):
    if isinstance(value, datetime):
        return get_apex_datetime(value)

    return f"'{value}'" if isinstance(value, str) else f"{value}"


def get_positive_int_input(message: str):
    while True:
        try:
            value = int(input(message))

            if value <= 0:
                raise ValueError()

            return value
        except ValueError:
            print("Invalid input. Please enter a valid positive integer.")
