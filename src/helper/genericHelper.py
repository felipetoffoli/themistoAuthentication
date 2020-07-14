import datetime
import re

class GenericHelper:

    def __init__(self):
        pass

    def str_date_to_datetime(self, str_date):
         return datetime.datetime.strptime(str_date, '%d/%m/%Y')

    def str_date_check(self, str_date):
        return re.fullmatch(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', str_date)
    
    def iso_date_to_local_date(self, date):
        if not date: return date
        iso_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        return format(iso_date, "%d/%m/%Y")
