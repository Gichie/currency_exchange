import sqlite3


class CurrencyRepository:
    @staticmethod
    def fetch_all():
        """
        Возвращает все записи из таблицы `currencies`.

        :return: Список строк из таблицы.
        """
        query = "SELECT * FROM currencies"
        return CurrencyRepository.execute_query(query)

    @staticmethod
    def fetch_by_code(code: str):
        """
        Возвращает запись валюты по её коду.

        :param code: Код валюты (например, "USD").
        :return: Строка с информацией о валюте или None, если запись не найдена.
        """
        query = "SELECT * FROM currencies WHERE code = ?"
        result = CurrencyRepository.execute_query(query, (code,))
        return result[0] if result else None

    @staticmethod
    def insert(name: str, code: str, sign: str):
        """
        Добавляет новую валюту в таблицу `currencies`.

        :param name: Полное название валюты (например, "US Dollar").
        :param code: Код валюты (например, "USD").
        :param sign: Символ валюты (например, "$").
        :return: Идентификатор вставленной записи.
        """
        query = "INSERT INTO currencies (FullName, Code, Sign) VALUES (?, ?, ?)"
        return CurrencyRepository.execute_query(query, (name, code, sign))

    @staticmethod
    def execute_query(query: str, params: tuple = ()):
        """
        Выполняет произвольный SQL-запрос.

        :param query: Текст SQL-запроса.
        :param params: Параметры для запроса (по умолчанию пустой кортеж).
        :return: Результат выполнения запроса.
                 - Для SELECT: Список строк.
                 - Для остальных запросов: Идентификатор последней вставленной записи.
        """
        try:
            conn = sqlite3.connect("database/currency_exchange.db")
            cursor = conn.cursor()
            cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid
            conn.close()
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
