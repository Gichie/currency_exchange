import sqlite3


def get_currencies_from_db():
    conn = sqlite3.connect("database/currency_exchange.db")  # Подключение к базе данных
    cursor = conn.cursor()

    # Выполнение SQL-запроса
    cursor.execute("SELECT ID, Code, FullName, Sign FROM Currencies")
    rows = cursor.fetchall()

    # Закрытие соединения
    conn.close()

    # Преобразование данных в список словарей
    currencies = [{'id': row[0], "name": row[2], "code": row[1], "symbol": row[3]} for row in rows]
    return currencies


# Обработчики маршрутов
def handle_routes(path, method, data=None):
    if method == "GET":
        if path == "/":
            return {"message": "Welcome to the backend!"}, 200
        elif path == "/currencies":
            currencies = get_currencies_from_db()  # Получение данных из базы
            return currencies, 200
        else:
            return {"error": "Not Found"}, 404

    elif method == "POST":
        if path == "/data":
            return {"received": data}, 200
        else:
            return {"error": "Not Found"}, 404
