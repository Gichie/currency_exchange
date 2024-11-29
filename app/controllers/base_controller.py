from app.controllers.currency_cotroller import CurrencyController
from app.controllers.exchange_rate_controller import ExchangeRateController
from app.view import ResponseBuilder



# Обработчики маршрутов
def handle_routes(path, method, data=None):
    if method == "GET":
        if path == "/":
            return ResponseBuilder.json_response({"message": "Welcome to the backend!"}, status=200)
        elif path == "/currencies":
            return CurrencyController().get_all_currencies()
        elif path.startswith("/currency/"):
            # Извлекаем код валюты из URL
            currency_code = path[len("/currency/"):].upper().strip()
            return CurrencyController.get_currency(currency_code)
        elif path.startswith("/exchangeRate/"):
            currency_pair = path[len("/exchangeRate/"):].upper().strip()
            return ExchangeRateController.get_exchange_rate(currency_pair)
        elif path == "/exchangeRates":
            return ExchangeRateController.get_all_exchange_rates()
        else:
            return ResponseBuilder.error_response("Not Found", status=404)

    elif method == "POST":
        if path == '/currencies':
            return CurrencyController.add_currency(data)
        elif path == '/exchangeRates':
            return ExchangeRateController.add_exchange_rate(data)
        else:
            return ResponseBuilder.error_response("Not Found", status=404)


