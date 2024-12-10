from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from app.routes.routes import route_request
from app.views.response_builder import ResponseBuilder


class MyHandler(BaseHTTPRequestHandler):
    def handle_request(self, method):
        """Обрабатывает запросы с маршрутизацией."""
        try:
            # Парсинг пути и запроса
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            query_params = parse_qs(parsed_url.query)

            # Чтение тела запроса, если это POST/PATCH
            data = None
            if method in ["POST", "PATCH"]:
                content_length = int(self.headers.get("Content-Length", 0))
                raw_data = self.rfile.read(content_length).decode("utf-8")
                if self.headers.get("Content-Type") == "application/x-www-form-urlencoded":
                    # Преобразование значений из списка в строки
                    parsed_data = parse_qs(raw_data)
                    data = {key: value[0] for key, value in parsed_data.items()}
                else:
                    data = {}

            # Роутинг
            response, status, content_type = route_request(self.path, method, data or query_params)

            # Отправка ответа
            self._send_response(response, status, content_type)

        except Exception as e:
            # Обработка ошибок
            print(f"Unhandled error during {method} request: {e}")
            response, status, content_type = ResponseBuilder.error_response(
                "Internal Server Error", status=500
            )
            self._send_response(response, status, content_type)

    def do_GET(self):
        """Обрабатывает GET-запросы."""
        self.handle_request("GET")

    def do_POST(self):
        """Обрабатывает POST-запросы."""
        self.handle_request("POST")

    def do_PATCH(self):
        """Обрабатывает PATCH-запросы."""
        self.handle_request("PATCH")

    def _send_response(self, response, status, content_type):
        """Формирует и отправляет HTTP-ответ."""
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(response)
