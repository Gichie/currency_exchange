from typing import Optional

from app.services.exchange_rate_service import ExchangeRateService
from app.views.response_builder import ResponseBuilder


class ExchangeRateController:
    @staticmethod
    def get_all_exchange_rates():
        '''
        Возвращает список всех доступных курсов валют.
        '''
        rates = ExchangeRateService.get_all_exchange_rates()
        return ResponseBuilder.json_response(rates, status=200)

    @staticmethod
    def get_exchange_rate(currency_pair: str):
        """
        Возвращает курс валют для указанной валютной пары.

        :param currency_pair: Валютная пара в формате "USDEUR".
        :return: JSON-ответ с курсом валют или ошибкой.
        """
        if not ExchangeRateController.is_valid_currency_pair(currency_pair):
            return ResponseBuilder.error_response("Invalid currency pair", status=400)
        base_currency, target_currency = ExchangeRateController.split_currency_pair(currency_pair)
        rate = ExchangeRateService.get_exchange_rate_by_pair(base_currency, target_currency)
        if not rate:
            return ResponseBuilder.error_response("Exchange rate not found", status=404)
        return ResponseBuilder.json_response(rate, status=200)

    @staticmethod
    def add_exchange_rate(data: dict):
        """
        Добавляет новый курс валют.

        :param data: Словарь с данными, содержащий baseCurrencyCode, targetCurrencyCode и rate.
        :return: JSON-ответ с результатом операции.
        """
        required_fields = ['baseCurrencyCode', 'targetCurrencyCode', 'rate']
        validation_error = ExchangeRateController.validate_required_fields(data, required_fields)
        if validation_error:
            return validation_error  # Возвращаем ошибку, если проверка не пройдена

        base_currency = data.get("baseCurrencyCode")
        target_currency = data.get("targetCurrencyCode")
        rate = data.get("rate")
        response, status = ExchangeRateService.add_exchange_rate(base_currency, target_currency, float(rate))
        return ResponseBuilder.json_response(response, status=status)

    @staticmethod
    def update_exchange_rate(currency_pair: str, data: dict):
        """
        Обновляет курс валют для указанной валютной пары.

        :param currency_pair: Валютная пара в формате "USDEUR".
        :param data: Словарь с данными, содержащий новое значение курса (rate).
        :return: JSON-ответ с результатом операции.
        """
        if not ExchangeRateController.is_valid_currency_pair(currency_pair):
            return ResponseBuilder.error_response("Invalid currency pair", status=400)

        validation_error = ExchangeRateController.validate_required_fields(data, ["rate"])
        if validation_error:
            return validation_error

        base_currency, target_currency = ExchangeRateController.split_currency_pair(currency_pair)
        rate = float(data.get("rate"))
        response, status = ExchangeRateService.update_exchange_rate(base_currency, target_currency, rate)
        return ResponseBuilder.json_response(response, status=status)

    @staticmethod
    def transfers_currency(from_currency: str, to_currency: str, amount: float):
        """
        Конвертирует валюту из одной в другую.

        :param from_currency: Код исходной валюты (например, "USD").
        :param to_currency: Код целевой валюты (например, "EUR").
        :param amount: Сумма для конвертации.
        :return: JSON-ответ с результатом конвертации или ошибкой.
        """
        try:
            # Преобразуем значения к верхнему регистру и числу
            from_currency = from_currency.upper()
            to_currency = to_currency.upper()
            amount = float(amount)

            # Вызываем сервис для расчета
            result, status = ExchangeRateService.calculate_exchange(from_currency, to_currency, amount)
            print(f"Result: {result}, Status: {status}")
            return ResponseBuilder.json_response(result, status=status)
        except ValueError as e:
            print(f"ValueError: {e}")
            return ResponseBuilder.error_response(str(e), status=400)
        except Exception as e:
            print(f"Unhandled error: {e}")
            return ResponseBuilder.error_response("Internal Server Error", status=500)

    @staticmethod
    def is_valid_currency_pair(currency_pair: str) -> bool:
        """
        Конвертирует валюту из одной в другую.

        :param from_currency: Код исходной валюты (например, "USD").
        :param to_currency: Код целевой валюты (например, "EUR").
        :param amount: Сумма для конвертации.
        :return: JSON-ответ с результатом конвертации или ошибкой.
        """
        return len(currency_pair) == 6

    @staticmethod
    def validate_required_fields(data: dict, required_fields: list[str]):
        """
        Проверяет наличие всех обязательных полей в данных.

        :param data: Словарь с данными.
        :param required_fields: Список обязательных полей.
        :return: None, если все поля есть, иначе JSON-ответ с ошибкой.
        """
        for field in required_fields:
            if field not in data or not data[field].strip():
                return ResponseBuilder.error_response(f"Missing required field: {field}", status=400)
        return None  # Если ошибок нет

    @staticmethod
    def split_currency_pair(currency_pair: str) -> tuple[str, str]:
        """
        Разделяет валютную пару на базовую и целевую валюты.

        :param currency_pair: Валютная пара в формате "USDEUR".
        :return: Кортеж из базовой валюты и целевой валюты.
        """
        return currency_pair[:3].upper(), currency_pair[3:].upper()
