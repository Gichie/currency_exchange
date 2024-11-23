from http.server import BaseHTTPRequestHandler

from app.controller import handle_routes  # Импорт обработчика маршрутов
from app.view import ResponseBuilder


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Передаем путь и метод в контроллер
            response_data, status, content_type = handle_routes(self.path, method="GET")

            # Используем представление для формирования ответа
            response_body, status, content_type = ResponseBuilder.json_response(
                response_data, status, content_type
            )
            self._send_response(response_body, status, content_type)
        except Exception as e:
            # Обрабатываем необработанные ошибки
            print(f"Unhandled error during GET request: {e}")
            response_body, status, content_type = ResponseBuilder.error_response(
                "Internal Server Error"
            )
            self._send_response(response_body, status, content_type)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            response_data, status, content_type = handle_routes(
                self.path, method="POST", data=post_data
            )
            response_body, status, content_type = ResponseBuilder.json_response(
                response_data, status, content_type
            )
            self._send_response(response_body, status, content_type)
        except Exception as e:
            print(f"Unhandled error during POST request: {e}")
            response_body, status, content_type = ResponseBuilder.error_response(
                "Internal Server Error"
            )
            self._send_response(response_body, status, content_type)

    def _send_response(self, body, status, content_type):
        """Формирует и отправляет ответ клиенту."""
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(body)
