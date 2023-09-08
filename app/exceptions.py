class MonthFormatException(Exception):

    def __init__(self, message: str, *args):
        self.message = f'Не найден месяц с таким ключём {message}'
        super().__init__(self.message, *args)
