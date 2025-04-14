from datetime import datetime


def get_apex_datetime(date: datetime):
    str_date = date.strftime('%d-%b-%y %I.%M.%S.%f %p %z')
    return f"'{str_date[:-2]}:{str_date[-2:]}'".upper()
