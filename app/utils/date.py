from dataclasses import dataclass
from datetime import datetime

from app.exceptions import MonthFormatException


@dataclass
class DateFormatter:
    str_date: str

    def __post_init__(self):
        self.months_lang_stock_dict = {
            'январ': 'january',
            'феврал': 'february',
            'март': 'march',
            'апрел': 'april',
            'ма': 'may',
            'июн': 'june',
            'июл': 'july',
            'август': 'august',
            'сентябр': 'september',
            'октябр': 'october',
            'ноябр': 'november',
            'декабр': 'december',
        }

    def parse_month(self, date_str: str):
        found_month: str | None = None
        for month_lang, native_month in self.months_lang_stock_dict.items():
            if month_lang in date_str:
                found_month = self.months_lang_stock_dict[month_lang]
                break
            found_month = month_lang
        else:
            raise MonthFormatException(found_month)
        return found_month

    @property
    def native_dates(self) -> list:
        split_date = self.str_date.replace('с', '', 1).strip().split(' по ')
        month_names = []
        dates = []
        datetime_dates = []
        for date_str in split_date:
            split_inner_date = date_str.split()
            if len(split_inner_date) > 1:
                date_month, month = split_inner_date
                try:
                    month_names.append(self.parse_month(month))
                    dates.append(int(date_month))
                except MonthFormatException as error:
                    print(error)
                    dates.append(int(date_month))
            else:
                dates.append(int(date_str))
        if len(month_names) < 2:
            month_names = month_names * 2
        year = datetime.today().year
        for date_, month in zip(dates, month_names):
            valid_date = datetime.strptime(
                f'{date_} {month} {year}', '%d %B %Y'
            )
            datetime_dates.append(valid_date.date())
        return datetime_dates
