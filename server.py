# Основной файл сервера
from http.server import HTTPServer

from app.routes.handler import MyHandler

# Импортируем обработчик запросов

HOST = '192.168.1.118'
PORT = 8080


def run():
    print(f"Server started at http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), MyHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()
