# Логика работы с базой данных
import sqlite3


class CurrencyModel:
    @staticmethod
    def get_all_currencies():
        query = "SELECT * FROM currencies"
        return get_currencies_from_db(query)

    @staticmethod
    def get_currency_by_code(code):
        """Проверяет, существует ли валюта с данным кодом."""
        try:
            conn = sqlite3.connect('database/currency_exchange.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM currencies WHERE code = ?", (code,))
            result = cursor.fetchone()
            conn.close()
            return result
        except sqlite3.Error as e:
            print(f"Database error in get_currency_by_code: {e}")
            raise

    @staticmethod
    def insert_currency(name, code, sign):
        """Добавляет новую валюту в базу данных."""
        try:
            conn = sqlite3.connect('database/currency_exchange.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO currencies (Code, FullName, Sign) VALUES (?, ?, ?)", (code, name, sign)
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Database error in insert_currency: {e}")
            raise


def get_currencies_from_db(query, params=()):
    """Функция для выполнения запросов к базе данных."""
    try:
        conn = sqlite3.connect("database/currency_exchange.db")  # Подключение к базе данных
        cursor = conn.cursor()

        # Выполнение SQL-запроса с параметрами
        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Закрытие соединения
        conn.close()

        # Преобразование данных в список словарей
        return rows

    except sqlite3.Error as e:
        # Логирование ошибки базы данных (опционально)
        print(f"Database error: {e}")
        raise  # Проброс исключения наверх
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
