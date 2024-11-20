# Основной файл сервера
from http.server import HTTPServer

from app.routes import MyHandler  # Импортируем обработчик запросов

HOST = '192.168.1.118'
PORT = 8080


def run():
    print('Server started http://{host}:{port}'.format(host=HOST, port=PORT))
    server = HTTPServer((HOST, PORT), MyHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()
