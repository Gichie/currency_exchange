# Логика работы с базой данных
import sqlite3


class CurrencyModel:
    @staticmethod
    def get_all_currencies():
        """
        Возвращает список всех валют из базы данных.

        :return: Список строк, представляющих валюты.
        """
        query = "SELECT * FROM currencies"
        return get_currencies_from_db(query)

    @staticmethod
    def get_currency_by_code(code: str):
        """
        Возвращает строку валюты по её коду.

        :param code: Код валюты (например, "USD").
        :return: Результат запроса (строка) или None, если валюта не найдена.
        """
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
    def insert_currency(name: str, code: str, sign: str):
        """
        Добавляет новую валюту в базу данных.

        :param name: Название валюты (например, "US Dollar").
        :param code: Код валюты (например, "USD").
        :param sign: Символ валюты (например, "$").
        :return: None.
        """
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


def get_currencies_from_db(query: str, params: tuple = ()):
    """
    Выполняет SQL-запрос к базе данных и возвращает результат.

    :param query: SQL-запрос.
    :param params: Параметры для запроса (по умолчанию пустой кортеж).
    :return: Результат запроса в виде списка строк.
    """
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
