import sqlite3

from app.models.exchange_rate_model import ExchangeRateModel
from app.services.currency_service import CurrencyService


class ExchangeRateService:
    @staticmethod
    def format_exchange_rate(row):
        return {
            "id": row[0],
            "base_currency": {
                "id": row[1],
                "code": row[2],
                "name": row[3],
                "sign": row[4]
            },
            "target_currency": {
                "id": row[5],
                "name": row[6],
                "code": row[7],
                "sign": row[8]
            },
            "rate": row[9]
        }

    @staticmethod
    def get_all_exchange_rates():
        rows = ExchangeRateModel.get_all_exchange_rates()
        return [ExchangeRateService.format_exchange_rate(row) for row in rows]

    @staticmethod
    def get_exchange_rate_by_pair(base_currency_code, target_currency_code):
        rows = ExchangeRateModel.get_exchange_rate_by_pair(base_currency_code, target_currency_code)
        if not rows:
            return None
        return ExchangeRateService.format_exchange_rate(rows[0])

    @staticmethod
    def add_exchange_rate(base_currency_code, target_currency_code, rate):
        # Проверяем, что обе валюты существуют
        base_currency_id = ExchangeRateModel.get_currency_id_by_code(base_currency_code)
        target_currency_id = ExchangeRateModel.get_currency_id_by_code(target_currency_code)

        if not base_currency_id or not target_currency_id:
            return {'error 404': "One or both currencies not founf"}, 404

        # Проверяем, что пара не существует
        if ExchangeRateModel.check_exchange_rate_exists(base_currency_id, target_currency_id):
            return {"error 409": "Exchange rate already exists"}, 409

        try:
            # Добавляем новый обменный курс
            ExchangeRateModel.add_exchange_rate(base_currency_id, target_currency_id, rate)
            return {"message": "Exchange rate added successfully"}, 201
        except sqlite3.Error:
            return {"error 500": "Internal Server Error"}, 500

    @staticmethod
    def update_exchange_rate(base_currency_code, target_currency_code, rate):
        """Обновляет существующий обменный курс."""
        # Получение данных валют
        base_currency = CurrencyService.get_currency(base_currency_code)
        target_currency = CurrencyService.get_currency(target_currency_code)

        if not base_currency:
            raise ValueError(f"Base currency '{base_currency_code}' not found")
        if not target_currency:
            raise ValueError(f"Target currency '{target_currency_code}' not found")

        # Обновление курса
        updated_row = ExchangeRateModel.update_exchange_rate(base_currency["id"], target_currency["id"], rate)

        if not updated_row:
            return None  # Курс для валютной пары не найден

        # Форматирование результата
        return ExchangeRateService.format_exchange_rate(updated_row)

    @staticmethod
    def calculate_exchange(base_currency, target_currency, amount):
        try:
            # Проверяем, существуют ли валюты
            base_currency = CurrencyService.get_currency(base_currency)
            target_currency = CurrencyService.get_currency(target_currency)

            if not base_currency:
                return {"error": f"Base currency '{base_currency}' not found"}
            if not target_currency:
                return {"error": f"Target currency '{target_currency}' not found"}

            # 1. Прямой курс A -> B
            direct_rate = ExchangeRateModel.get_exchange_rate_by_pair(base_currency['code'], target_currency['code'])
            if direct_rate:
                rate = direct_rate[0][9]  # Курс находится в 9-й колонке
                converted_amount = amount * rate
                return ExchangeRateService.format_exchange_response(base_currency, target_currency, rate, amount,
                                                                    converted_amount)

            # 2. Обратный курс B -> A
            reverse_rate = ExchangeRateModel.get_exchange_rate_by_pair(target_currency['code'], base_currency['code'])
            if reverse_rate:
                rate = 1 / reverse_rate[0][9]
                converted_amount = amount * rate
                return ExchangeRateService.format_exchange_response(base_currency, target_currency, rate, amount,
                                                                    converted_amount)

            # 3. Вычисляем через USD (или базовую валюту системы)
            usd_to_base = ExchangeRateModel.get_exchange_rate_by_pair("USD", base_currency['code'])
            usd_to_target = ExchangeRateModel.get_exchange_rate_by_pair("USD", target_currency['code'])
            if usd_to_base and usd_to_target:
                rate = (1 / usd_to_base[0][9]) * usd_to_target[0][9]
                converted_amount = amount * rate
                return ExchangeRateService.format_exchange_response(base_currency, target_currency, rate, amount,
                                                                    converted_amount)

            return {"error": f"Exchange rate not found for pair '{base_currency}' to '{target_currency}'"}
        except Exception as e:
            print(f"Error in calculate_exchange: {e}")
            raise

    @staticmethod
    def format_exchange_response(base_currency, target_currency, rate, amount, converted_amount):
        """Форматирует ответ конвертации."""
        return {
            "baseCurrency": {
                "id": base_currency["id"],
                "name": base_currency["name"],
                "code": base_currency["code"],
                "sign": base_currency["symbol"],
            },
            "targetCurrency": {
                "id": target_currency["id"],
                "name": target_currency["name"],
                "code": target_currency["code"],
                "sign": target_currency["symbol"],
            },
            "rate": round(rate, 4),
            "amount": round(amount, 2),
            "convertedAmount": round(converted_amount, 2),
        }
