from app.services.currency_service import CurrencyService  # Работа с бизнес-логикой
from app.services.exchange_rate_service import ExchangeRateService


# Обработчики маршрутов
def handle_routes(path, method, data=None):
    if method == "GET":
        if path == "/":
            return {"message": "Welcome to the backend!"}, 200, "application/json"  # Возвращаем content_type

        elif path == "/currencies":
            try:
                currencies = CurrencyService.get_all_currencies()  # Получение данных из базы
                return currencies, 200, "application/json"
            except Exception:
                return {"error 500": "Internal Server Error"}, 500, "application/json"

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

        elif path == "/exchangeRates":
            try:
                exchange_rates = ExchangeRateService.get_all_exchange_rates()  # Получение всех обменных курсов из БД
                return exchange_rates, 200, "application/json"
            except Exception:
                return {"error 500": "Internal Server Error"}, 500, "application/json"


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

        else:
            return {"error 404": "Not Found"}, 404, "application/json"
