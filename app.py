# Основной файл сервера
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from routes import handle_routes

HOST = '192.168.1.118'
PORT = 8080


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Динамическая маршрутизация
        response, status = handle_routes(self.path, method="GET")
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(post_data)  # Ожидаем JSON
        except json.JSONDecodeError:
            data = {"error": "Invalid JSON"}

        # Динамическая маршрутизация
        response, status = handle_routes(self.path, method="POST", data=data)
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))


def run():
    print('Server started http://{host}:{port}'.format(host=HOST, port=PORT))
    server = HTTPServer((HOST, PORT), MyHandler)
    server.serve_forever()

if __name__ == "__main__":
    run()
