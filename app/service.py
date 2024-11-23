# Логика преобразования данных в словари
from app.model import CurrencyModel


class CurrencyService:
    @staticmethod
    def format_currency_row(row):
        return {"id": row[0], "name": row[2], "code": row[1], "symbol": row[3]}

    @staticmethod
    def get_all_currencies():
        rows = CurrencyModel.get_all_currencies()
        return [CurrencyService.format_currency_row(row) for row in rows]

    @staticmethod
    def get_currency(code):
        rows = CurrencyModel.get_currency_by_code(code)
        if rows:
            return CurrencyService.format_currency_row(rows[0])
        return None
