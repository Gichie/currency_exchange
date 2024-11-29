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
                return currencies, 200, "application/json"
            except Exception:
                return ResponseBuilder.error_response("Internal Server Error", status=500)

        elif path.startswith("/currency/"):
            # Извлекаем код валюты из URL
            currency_code = path[len("/currency/"):].upper().strip()
            if not currency_code:
                return {"error 400": "Currency code is missing in the URL"}, 400, "application/json"
            try:
                # Поиск валюты в базе данных
                currency = CurrencyService.get_currency(currency_code)
                if not currency:  # Если результат пустой
                    return {"error 404": f"Currency '{currency_code}' not found"}, 404, "application/json"
                return currency, 200, "application/json"
            except Exception:
                return {"error 500": "Internal Server Error"}, 500, "application/json"

        elif path.startswith("/exchangeRate/"):
            base_currency = path[len("/exchangeRate/"):-3].upper().strip()
            target_currency = path[len("/exchangeRate/") + 3:].upper().strip()
            if not base_currency or not target_currency:
                return {"error 400": "Currency codes of the pair are missing in the URL"}, 400, "application/json"
            try:
                # Получаем обменный курс через сервис
                exchange_rate = ExchangeRateService.get_exchange_rate_by_pair(base_currency, target_currency)
                if not exchange_rate:
                    return {
                        "error 404": f"Exchange rate for pair '{base_currency}{target_currency}' not found"}, 404, "application/json"
                return exchange_rate, 200, "application/json"
            except Exception:
                return {"error 500": "Internal Server Error"}, 500, "application/json"

        elif path == "/exchangeRates":
            try:
                exchange_rates = ExchangeRateService.get_all_exchange_rates()  # Получение всех обменных курсов из БД
                return ResponseBuilder.json_response(exchange_rates, status=200)
            except Exception:
                return ResponseBuilder.error_response("Internal Server Error", status=500)

        else:
            return {"error 404": "Not Found"}, 404, "application/json"

    elif method == "POST":
        if path == "/data":
            return {"received": data}, 200, "application/json"

        elif path == '/currencies':
            try:
                # Проверяем, переданы ли все необходимые данные
                required_fields = ["name", "code", "sign"]
                for field in required_fields:
                    if field not in data or not data[field].strip():
                        return {"error 400": f"Missing required field: {field}"}, 400, "application/json"

                # Добавляем валюту через сервис
                result = CurrencyService.add_currency(data['name'], data['code'], data['sign'])
                if result == 'exists':
                    return {'error 409': "Currency with this code already exists"}, 409, "application/json"
                elif result == 'success':
                    return {"message": "Currency added successfully"}, 201, "application/json"
            except Exception:
                return {"error 500": "Internal Server Error"}, 500, "application/json"

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
                return {"error 400": f"Invalid rate format"}, 400, "application/json"

            # Добавляем новый обменный курс через сервис
            response, status = ExchangeRateService.add_exchange_rate(base_currency_code, target_currency_code, rate)
            return response, status, "application/json"

        else:
            return ResponseBuilder.error_response("Not Found", status=404)
