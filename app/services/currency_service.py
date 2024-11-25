# Логика преобразования данных в словари
from app.models.currency_model import CurrencyModel  # Работа с моделью


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
            return CurrencyService.format_currency_row(rows)
        return None

    @staticmethod
    def add_currency(name, code, sign):
        try:
            # Проверяем, существует ли валюта с таким кодом
            existing_currency = CurrencyModel.get_currency_by_code(code)
            if existing_currency:
                return 'exists'

            # Добавляем новую валюту
            CurrencyModel.insert_currency(name, code, sign)
            return 'success'

        except Exception as e:
            print(f"Error in CurrencyService.add_currency: {e}")
            raise
