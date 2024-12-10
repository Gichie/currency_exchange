from app.repositories.currency_repository import CurrencyRepository


class CurrencyService:
    @staticmethod
    def get_all_currencies():
        rows = CurrencyRepository.fetch_all()
        return [CurrencyService.format_currency(row) for row in rows]

    @staticmethod
    def get_currency_by_code(code):
        """Возвращает валюту по коду."""
        currency = CurrencyRepository.fetch_by_code(code)
        if not currency:
            return None  # Возвращаем None, если валюта не найдена

        # Преобразуем запись в словарь
        return CurrencyService.format_currency(currency)

    @staticmethod
    def add_currency(data):
        name, code, sign = data.get("name"), data.get("code"), data.get("sign")
        if CurrencyRepository.fetch_by_code(code):
            return {"error": "Currency already exists"}, 409
        CurrencyRepository.insert(name, code, sign)
        return {"message": "Currency added successfully"}, 201

    @staticmethod
    def format_currency(row):
        return {"id": row[0], "name": row[1], "code": row[2], "sign": row[3]}
