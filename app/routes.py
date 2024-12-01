from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

from app.controllers.base_controller import handle_routes  # Импорт обработчика маршрутов
from app.view import ResponseBuilder


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Передача запроса в обработчик маршрутов
            response, status, content_type = handle_routes(self.path, method="GET")
            self.send_response(status)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(response)

        except Exception as e:
            # Логирование и возврат ошибки
            response, status, content_type = ResponseBuilder.error_response(
                "Internal Server Error", status=500
            )
            self.send_response(status)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(response)
            print(f"Unhandled error during GET request: {e}")

    def do_POST(self):
        try:
            # Читаем данные из тела запроса
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Разбор данных формы
            if self.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
                data = parse_qs(post_data)
                # Преобразование значений из списка в строки
                data = {key: value[0] for key, value in data.items()}
            else:
                data = {}

            # Передача данных в обработчик маршрутов
            response, status, content_type = handle_routes(self.path, method="POST", data=data)
            self.send_response(status)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(response)
        except Exception as e:
            # Логирование и возврат ошибки
            response, status, content_type = ResponseBuilder.error_response(
                "Internal Server Error", status=500
            )
            self.send_response(status)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(response)
            print(f"Unhandled error during POST request: {e}")

    def do_PATCH(self):
        try:
            # Извлечение пути
            path = self.path

            # Чтение тела запроса
            content_length = int(self.headers.get('Content-Length', 0))
            patch_data = self.rfile.read(content_length).decode('utf-8')

            # Разбор данных формы
            if self.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
                data = parse_qs(patch_data)
                data = {key: value[0] for key, value in data.items()}
            else:
                data = {}

            # Передача маршрута в обработчик
            response, status, content_type = handle_routes(path, method="PATCH", data=data)

            # Ответ клиенту
            self.send_response(status)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(response)

        except Exception as e:
            # Возврат ошибки
            response, status, content_type = ResponseBuilder.error_response(
                "Internal Server Error", status=500
            )
            self.send_response(status)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(response)
            print(f"Unhandled error during PATCH request: {e}")

    def _send_response(self, body, status, content_type):
        """Формирует и отправляет ответ клиенту."""
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(body)
