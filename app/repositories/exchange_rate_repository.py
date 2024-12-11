import sqlite3


class ExchangeRateRepository:
    @staticmethod
    def fetch_all():
        """
        Возвращает все записи из таблицы `ExchangeRates` с подробной информацией о базовой и целевой валюте.

        :return: Список строк с информацией об обменных курсах.
        """
        query = """
            SELECT 
                er.ID,
                bc.ID AS BaseCurrencyId,
                bc.Code AS BaseCurrencyCode,
                bc.FullName AS BaseCurrencyName,
                bc.Sign AS BaseCurrencySign,
                tc.ID AS TargetCurrencyId,
                tc.Code AS TargetCurrencyCode,
                tc.FullName AS TargetCurrencyName,
                tc.Sign AS TargetCurrencySign,
                er.Rate
            FROM ExchangeRates AS er
            JOIN Currencies AS bc ON er.BaseCurrencyId = bc.ID
            JOIN Currencies AS tc ON er.TargetCurrencyId = tc.ID
        """
        return ExchangeRateRepository.execute_query(query)

    @staticmethod
    def fetch_by_pair(base_currency_code: str, target_currency_code: str):
        """
        Возвращает запись обменного курса для заданной пары валют.

        :param base_currency_code: Код базовой валюты (например, "USD").
        :param target_currency_code: Код целевой валюты (например, "EUR").
        :return: Список строк с информацией об обменном курсе или пустой список, если курс не найден.
        """
        query = """
            SELECT 
                er.ID,
                bc.ID AS BaseCurrencyId,
                bc.Code AS BaseCurrencyCode,
                bc.FullName AS BaseCurrencyName,
                bc.Sign AS BaseCurrencySign,
                tc.ID AS TargetCurrencyId,
                tc.Code AS TargetCurrencyCode,
                tc.FullName AS TargetCurrencyName,
                tc.Sign AS TargetCurrencySign,
                er.Rate
            FROM ExchangeRates AS er
            JOIN Currencies AS bc ON er.BaseCurrencyId = bc.ID
            JOIN Currencies AS tc ON er.TargetCurrencyId = tc.ID
            WHERE bc.Code = ? AND tc.Code = ?
        """
        return ExchangeRateRepository.execute_query(query, (base_currency_code, target_currency_code))

    @staticmethod
    def insert(base_currency_id: int, target_currency_id: int, rate: float):
        """
        Добавляет новую запись обменного курса.

        :param base_currency_id: Идентификатор базовой валюты.
        :param target_currency_id: Идентификатор целевой валюты.
        :param rate: Курс обмена.
        :return: Идентификатор вставленной записи.
        """
        query = """
            INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate)
            VALUES (?, ?, ?)
        """
        return ExchangeRateRepository.execute_query(query, (base_currency_id, target_currency_id, rate))

    @staticmethod
    def update(base_currency_id: int, target_currency_id: int, rate: float):
        """
        Обновляет существующую запись обменного курса.

        :param base_currency_id: Идентификатор базовой валюты.
        :param target_currency_id: Идентификатор целевой валюты.
        :param rate: Новый курс обмена.
        :return: Количество обновлённых строк.
        """
        query = """
            UPDATE ExchangeRates
            SET Rate = ?
            WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?
        """
        return ExchangeRateRepository.execute_query(query, (rate, base_currency_id, target_currency_id))

    @staticmethod
    def execute_query(query: str, params: tuple = ()):
        """
        Выполняет произвольный SQL-запрос.

        :param query: Текст SQL-запроса.
        :param params: Параметры для SQL-запроса (по умолчанию пустой кортеж).
        :return: Результат выполнения запроса.
                 - Для SELECT: Список строк.
                 - Для остальных запросов: Идентификатор последней вставленной записи.
        """
        try:
            conn = sqlite3.connect("database/currency_exchange.db")
            cursor = conn.cursor()
            print(f"Executing query: {query} with params: {params}")
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
