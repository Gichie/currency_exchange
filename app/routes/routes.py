'''
Модуль маршрутизации запросов
'''
import re
from urllib.parse import urlparse

from app.controllers.currency_cotroller import CurrencyController
from app.controllers.exchange_rate_controller import ExchangeRateController
from app.views.response_builder import ResponseBuilder

# Словарь маршрутов
routes = {
    "GET": {
        "/": CurrencyController.home,
        "/currencies": CurrencyController.get_all_currencies,
        r"/currency/(?P<code>\w{3})": CurrencyController.get_currency,
        r"/exchangeRate/(?P<pair>\w{6})": ExchangeRateController.get_exchange_rate,
        "/exchangeRates": ExchangeRateController.get_all_exchange_rates,
        r"/exchange": ExchangeRateController.transfers_currency,
    },
    "POST": {
        "/currencies": CurrencyController.add_currency,
        "/exchangeRates": ExchangeRateController.add_exchange_rate,
    },
    "PATCH": {
        r"/exchangeRate/(?P<pair>\w{6})": ExchangeRateController.update_exchange_rate,
    },
}


def extract_query_params(query_string: str) -> dict:
    """
    Извлекает параметры из строки запроса.

    :param query_string: Строка запроса (например, "key1=value1&key2=value2").
    :return: Словарь параметров.
    """
    if not query_string:
        return {}
    try:
        # Разбираем строку вручную
        params = {}
        for pair in query_string.split("&"):
            key, value = pair.split("=")
            params[key] = value
        return params
    except ValueError:
        print("Invalid query string format")
        return {}


def route_request(path: str, method: str, data: dict = None) -> tuple:
    """
    Ищет соответствие маршрута и вызывает соответствующий контроллер.

    :param path: Путь URL (например, "/currency/USD").
    :param method: HTTP-метод запроса (GET, POST, PATCH).
    :param data: Тело запроса (опционально для POST/PATCH).
    :return: Кортеж (response, status, content_type) или HTTP-ответ об ошибке.
    """
    try:
        # Разбираем URL на путь и параметры строки запроса
        parsed_url = urlparse(path)
        clean_path = parsed_url.path
        query_params = extract_query_params(parsed_url.query)

        print(f"Raw path: {path}")
        print(f"Parsed URL: {parsed_url}")
        print(f"Query params (manual parsing): {query_params}")

        if not query_params:
            print("Warning: Query params are empty. Check the request format.")

        method_routes = routes.get(method, {})
        for route, handler in method_routes.items():
            print(f"Trying route: {route}")
            # Используем регулярное выражение для сопоставления пути
            match = re.fullmatch(route, clean_path)
            if match:
                print(f"Matched route: {route}")
                # Извлекаем параметры маршрута
                route_params = match.groupdict()

                # Приведение параметров к верхнему регистру, если необходимо
                for param in ["code", "pair", "from_currency", "to_currency"]:
                    if param in route_params:
                        route_params[param] = route_params[param].upper()

                # Если есть параметры строки запроса, объединяем их с route_params
                if query_params:
                    # Преобразуем значения query_params из списков в строки
                    query_params = {key: value for key, value in query_params.items()}
                    route_params.update(query_params)

                # Передача параметров:
                if method in ["POST", "PATCH"]:
                    # Для POST/PATCH передаем параметры маршрута и тело запроса
                    return handler(*route_params.values(), data)
                else:
                    # Для остальных методов передаем только позиционные параметры
                    return handler(*route_params.values())

        # Если маршрут не найден
        return ResponseBuilder.error_response("Route not found", status=404)
    except Exception as e:
        print(f"Error in route_request: {e}")
        return ResponseBuilder.error_response("Internal Server Error", status=500)
