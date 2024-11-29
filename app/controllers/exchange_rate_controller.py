from app.services.exchange_rate_service import ExchangeRateService
from app.view import ResponseBuilder


class ExchangeRateController:
    @staticmethod
    def get_exchange_rate(currency_pair):
        if len(currency_pair) != 6:
            return ResponseBuilder.error_response("Invalid currency pair", status=400)
        try:
            base_currency = currency_pair[:3].upper()
            target_currency = currency_pair[3:].upper()
            exchange_rate = ExchangeRateService.get_exchange_rate_by_pair(base_currency, target_currency)
            if not exchange_rate:
                return ResponseBuilder.error_response("Exchange rate not found", status=404)
            return ResponseBuilder.json_response(exchange_rate, status=200)
        except Exception as e:
            print(f"Error in ExchangeRateController.get_exchange_rate: {e}")
            return ResponseBuilder.error_response("Internal Server Error", status=500)

    @staticmethod
    def add_exchange_rate(data):
        """Добавляет новый обменный курс."""
        required_fields = ['baseCurrencyCode', 'targetCurrencyCode', 'rate']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return ResponseBuilder.error_response(
                    {"error": f"Missing required field: {field}"}, status=400
                )

        base_currency_code = data.get("baseCurrencyCode").strip().upper()
        target_currency_code = data.get("targetCurrencyCode").strip().upper()
        try:
            rate = float(data.get("rate"))
        except ValueError:
            return ResponseBuilder.error_response({"error": "Invalid rate format"}, status=400)

        try:
            # Используем сервис для добавления нового обменного курса
            response, status = ExchangeRateService.add_exchange_rate(base_currency_code, target_currency_code, rate)
            return ResponseBuilder.json_response(response, status=status)
        except Exception as e:
            print(f"Error in ExchangeRateController.add_exchange_rate: {e}")
            return ResponseBuilder.error_response("Internal Server Error", status=500)


    @staticmethod
    def get_all_exchange_rates():
        """Возвращает все обменные курсы из базы данных."""
        try:
            exchange_rates = ExchangeRateService.get_all_exchange_rates()
            return ResponseBuilder.json_response(exchange_rates, status=200)
        except Exception as e:
            print(f"Error in ExchangeRateController.get_all_exchange_rates: {e}")
            return ResponseBuilder.error_response("Internal Server Error", status=500)

    @staticmethod
    def update_exchange_rate(currency_pair, rate):
        """Обновляет курс обмена по указанной валютной паре."""
        if len(currency_pair) != 6:
            return ResponseBuilder.error_response("Invalid currency pair", status=400)
        try:
            base_currency = currency_pair[:3].upper()
            target_currency = currency_pair[3:].upper()
            response, status = ExchangeRateService.update_exchange_rate(base_currency, target_currency, rate)
            return ResponseBuilder.json_response(response, status=status)
        except Exception as e:
            print(f"Error in ExchangeRateController.update_exchange_rate: {e}")
            return ResponseBuilder.error_response("Internal Server Error", status=500)
