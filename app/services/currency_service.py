'''
Модуль предоставляет бизнес-логику для управления валютами. Использует `CurrencyRepository` для работы с базой данных и добавляет дополнительную обработку данных.
'''
from app.repositories.currency_repository import CurrencyRepository


class CurrencyService:
    @staticmethod
    def get_all_currencies() -> list[dict]:
        """
        Возвращает список всех валют, отформатированных в виде словарей.

        :return: Список словарей с информацией о валютах.
        """
        rows = CurrencyRepository.fetch_all()
        return [CurrencyService.format_currency(row) for row in rows]

    @staticmethod
    def get_currency_by_code(code: str) -> dict | None:
        """
        Возвращает информацию о валюте по её коду.

        :param code: Код валюты (например, "USD").
        :return: Словарь с информацией о валюте или None, если валюта не найдена.
        """
        currency = CurrencyRepository.fetch_by_code(code)
        if not currency:
            return None  # Возвращаем None, если валюта не найдена

        # Преобразуем запись в словарь
        return CurrencyService.format_currency(currency)

    @staticmethod
    def add_currency(data: dict) -> tuple[dict, int]:
        """
        Добавляет новую валюту в базу данных.

        :param data: Словарь с данными валюты. Должен содержать:
            - name: Название валюты.
            - code: Код валюты.
            - sign: Символ валюты.
        :return: Кортеж (ответ в виде словаря, HTTP-статус).
        """
        name, code, sign = data.get("name"), data.get("code"), data.get("sign")
        if CurrencyRepository.fetch_by_code(code):
            return {"error": "Currency already exists"}, 409
        CurrencyRepository.insert(name, code, sign)
        return {"message": "Currency added successfully"}, 201

    @staticmethod
    def format_currency(row: tuple) -> dict:
        """
        Преобразует запись из базы данных в словарь.

        :param row: Кортеж с информацией о валюте (ID, имя, код, символ).
        :return: Словарь с полями "id", "name", "code", "sign".
        """
        return {"id": row[0], "name": row[1], "code": row[2], "sign": row[3]}
