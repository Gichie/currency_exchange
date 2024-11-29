from app.services.currency_service import CurrencyService  # Работа с бизнес-логикой
from app.services.exchange_rate_service import ExchangeRateService
from app.view import ResponseBuilder


# Обработчики маршрутов
def handle_routes(path, method, data=None):
    if method == "GET":
        if path == "/":
            return ResponseBuilder.json_response({"message": "Welcome to the backend!"}, status=200)

        elif path == "/currencies":
            try:
                currencies = CurrencyService.get_all_currencies()  # Получение данных из базы
                return ResponseBuilder.json_response(currencies, status=200)
            except Exception as e:
                print(f"Error handling /currencies: {e}")
                return ResponseBuilder.error_response("Internal Server Error", status=500)

        elif path.startswith("/currency/"):
            # Извлекаем код валюты из URL
            currency_code = path[len("/currency/"):].upper().strip()
            if not currency_code:
                return ResponseBuilder.error_response({"error 400": "Currency code is missing in the URL"}, status=400)
            try:
                # Поиск валюты в базе данных
                currency = CurrencyService.get_currency(currency_code)
                if not currency:  # Если результат пустой
                    return ResponseBuilder.error_response({"error 404": "Currency not found"}, status=404)
                return ResponseBuilder.json_response(currency, status=200)
            except Exception:
                return ResponseBuilder.error_response({"error 500": "Internal Server Error"}, status=500)

        elif path.startswith("/exchangeRate/"):
            base_currency = path[len("/exchangeRate/"):-3].upper().strip()
            target_currency = path[len("/exchangeRate/") + 3:].upper().strip()
            if not base_currency or not target_currency:
                return ResponseBuilder.error_response({"error 400": "Base currency is missing in the URL"}, status=400)
            try:
                # Получаем обменный курс через сервис
                exchange_rate = ExchangeRateService.get_exchange_rate_by_pair(base_currency, target_currency)
                if not exchange_rate:
                    return ResponseBuilder.error_response(
                        {"error 404": f"Exchange rate for pair '{base_currency}{target_currency}' not found"},
                        status=404)
                return ResponseBuilder.json_response(exchange_rate, status=200)
            except Exception:
                return ResponseBuilder.error_response({"error 500": "Internal Server Error"}, status=500)

        elif path == "/exchangeRates":
            try:
                exchange_rates = ExchangeRateService.get_all_exchange_rates()  # Получение всех обменных курсов из БД
                return ResponseBuilder.json_response(exchange_rates, status=200)
            except Exception:
                return ResponseBuilder.error_response("Internal Server Error", status=500)

        else:
            return ResponseBuilder.error_response("Not Found", status=404)

    elif method == "POST":
        if path == '/currencies':
            try:
                # Проверяем, переданы ли все необходимые данные
                required_fields = ["name", "code", "sign"]
                for field in required_fields:
                    if field not in data or not data[field].strip():
                        return ResponseBuilder.error_response({f'error 400": "Missing field: {field}'}, status=400)

                # Добавляем валюту через сервис
                result = CurrencyService.add_currency(data['name'], data['code'], data['sign'])
                if result == 'exists':
                    return ResponseBuilder.error_response("Currency already exists", status=409)
                elif result == 'success':
                    return ResponseBuilder.json_response({"message": "Currency added successfully"}, status=201)
            except Exception:
                return ResponseBuilder.error_response("Internal Server Error", status=500)

        elif path == '/exchangeRates':
            # Проверяем, переданы ли все необходимые данные
            required_fields = ['baseCurrencyCode', 'targetCurrencyCode', 'rate']
            for field in required_fields:
                if field not in data or not data[field].strip():
                    return ResponseBuilder.error_response(
                        f"Missing required field: {field}", status=400
                    )

            base_currency_code = data.get("baseCurrencyCode").strip().upper()
            target_currency_code = data.get("targetCurrencyCode").strip().upper()
            try:
                rate = float(data.get("rate"))
            except ValueError:
                return ResponseBuilder.error_response({"error 400": f"Invalid rate format"}, 400)

            # Добавляем новый обменный курс через сервис
            response, status = ExchangeRateService.add_exchange_rate(base_currency_code, target_currency_code, rate)
            return ResponseBuilder.json_response(response, status=status)

        else:
            return ResponseBuilder.error_response("Not Found", status=404)
