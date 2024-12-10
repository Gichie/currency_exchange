import sqlite3

from app.models.exchange_rate_model import ExchangeRateModel
from app.repositories.currency_repository import CurrencyRepository
from app.repositories.exchange_rate_repository import ExchangeRateRepository


class ExchangeRateService:
    @staticmethod
    def get_all_exchange_rates():
        rows = ExchangeRateRepository.fetch_all()
        return [ExchangeRateService.format_exchange_rate(row) for row in rows]

    @staticmethod
    def get_exchange_rate_by_pair(base_currency_code, target_currency_code):
        row = ExchangeRateRepository.fetch_by_pair(base_currency_code, target_currency_code)
        return ExchangeRateService.format_exchange_rate(row[0]) if row else None

    @staticmethod
    def add_exchange_rate(base_currency_code, target_currency_code, rate):
        base_currency = CurrencyRepository.fetch_by_code(base_currency_code)
        target_currency = CurrencyRepository.fetch_by_code(target_currency_code)

        if not base_currency or not target_currency:
            return {"error": "One or both currencies not found"}, 404

        if ExchangeRateRepository.fetch_by_pair(base_currency_code, target_currency_code):
            return {"error": "Exchange rate already exists"}, 409

        try:
            # Добавляем новый обменный курс
            ExchangeRateRepository.insert(base_currency[0], target_currency[0], rate)
            return {"message": "Exchange rate added successfully"}, 201
        except sqlite3.Error as e:
            return {"error": f"Database error: {e}"}, 500

    @staticmethod
    def update_exchange_rate(base_currency_code, target_currency_code, rate):
        base_currency = CurrencyRepository.fetch_by_code(base_currency_code)
        target_currency = CurrencyRepository.fetch_by_code(target_currency_code)

        if not base_currency or not target_currency:
            return {"error": "One or both currencies not found"}, 404

        if not ExchangeRateRepository.fetch_by_pair(base_currency_code, target_currency_code):
            return {"error": "Exchange rate not found"}, 404

        ExchangeRateRepository.update(base_currency[0], target_currency[0], rate)
        return {"message": "Exchange rate updated successfully"}, 200

    @staticmethod
    def calculate_exchange(base_currency_code, target_currency_code, amount):
        """
        Рассчитывает обмен валюты.
        """
        try:
            # Прямой курс (A -> B)
            exchange_rate = ExchangeRateRepository.fetch_by_pair(base_currency_code, target_currency_code)
            if exchange_rate:
                rate = exchange_rate[0][9]
                converted_amount = amount * rate
                return ExchangeRateService.format_conversion_result(base_currency_code, target_currency_code, rate,
                                                                    amount,
                                                                    converted_amount), 200
            # Обратный курс (B -> A)
            reverse_rate = ExchangeRateRepository.fetch_by_pair(target_currency_code, base_currency_code)
            if reverse_rate:
                rate = 1 / reverse_rate[0][9]
                converted_amount = amount * rate
                return ExchangeRateService.format_conversion_result(base_currency_code, target_currency_code, rate,
                                                                    amount,
                                                                    converted_amount), 200

            # Курс через третью валюту (например, USD)
            intermediate_rate_base = ExchangeRateModel.get_exchange_rate_by_pair("USD", base_currency_code)
            intermediate_rate_target = ExchangeRateModel.get_exchange_rate_by_pair("USD", target_currency_code)
            if intermediate_rate_base and intermediate_rate_target:
                rate = (1 / intermediate_rate_base[0][9]) * intermediate_rate_target[0][9]
                converted_amount = amount * rate
                result = ExchangeRateService.format_conversion_result(
                    base_currency_code,
                    target_currency_code,
                    rate,
                    amount,
                    converted_amount
                )
                return result, 200

            return {"error": "Exchange rate not found"}, 404

        except Exception as e:
            print(f"Error in calculate_exchange: {e}")
            return {"error": "Internal Server Error"}, 500

    @staticmethod
    def format_exchange_rate(row):
        return {
            "id": row[0],
            "base_currency": {"id": row[1], "code": row[2], "name": row[3], "sign": row[4]},
            "target_currency": {"id": row[5], "code": row[6], "name": row[7], "sign": row[8]},
            "rate": row[9],
        }

    @staticmethod
    def format_conversion_result(base_currency_code, target_currency_code, rate, amount, converted_amount):
        return {
            "baseCurrency": base_currency_code,
            "targetCurrency": target_currency_code,
            "rate": round(rate, 4),
            "amount": round(amount, 2),
            "convertedAmount": round(converted_amount, 2),
        }
