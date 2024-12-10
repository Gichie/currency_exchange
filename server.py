# Основной файл сервера
import os
from http.server import HTTPServer

from app.routes.handler import MyHandler

# Импортируем обработчик запросов

HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 8080))  # Получаем PORT из окружения


def run():
    print(f"Server started at http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), MyHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()
