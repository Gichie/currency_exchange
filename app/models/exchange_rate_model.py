import sqlite3


class ExchangeRateModel:
    @staticmethod
    def get_all_exchange_rates():
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
        return get_exchange_rates_from_db(query)

    @staticmethod
    def get_exchange_rate_by_pair(base_currency_code, target_currency_code):
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
        return get_exchange_rates_from_db(query, (base_currency_code, target_currency_code))

    @staticmethod
    def get_currency_id_by_code(currency_code):
        query = 'SELECT ID FROM Currencies WHERE Code = ?'
        result = get_exchange_rates_from_db(query, (currency_code,))
        return result[0][0] if result else None

    @staticmethod
    def check_exchange_rate_exists(base_currency_id, target_currency_id):
        query = "SELECT 1 FROM ExchangeRates WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?"
        result = get_exchange_rates_from_db(query, (base_currency_id, target_currency_id))
        return bool(result)

    @staticmethod
    def add_exchange_rate(base_currency_id, target_currency_id, rate):
        """Добавляет обменный курс в базу данных."""
        try:
            conn = sqlite3.connect('database/currency_exchange.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate) VALUES (?, ?, ?)",
                (base_currency_id, target_currency_id, rate)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database error in add_exchange_rate: {e}")
            raise

    @staticmethod
    def update_exchange_rate(base_currency_id: int, target_currency_id: int, rate: float):
        """Обновляет существующий обменный курс в базе данных."""
        try:
            conn = sqlite3.connect('database/currency_exchange.db')
            cursor = conn.cursor()
            # Обновление курса
            cursor.execute(
                """
                UPDATE ExchangeRates
                SET Rate = ?
                WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?
                """,
                (rate, base_currency_id, target_currency_id)
            )

            # Проверка количества обновлённых строк
            print(f"Rows updated: {cursor.rowcount}")
            if cursor.rowcount == 0:
                conn.close()
                return None  # Обменный курс не найден

            # Фиксация изменений
            conn.commit()

            # Получение обновлённой строки
            cursor.execute(
                """
                SELECT er.ID, 
                       bc.ID, bc.Code, bc.FullName, bc.Sign,
                       tc.ID, tc.Code, tc.FullName, tc.Sign, 
                       er.Rate
                FROM ExchangeRates er
                JOIN Currencies bc ON er.BaseCurrencyId = bc.ID
                JOIN Currencies tc ON er.TargetCurrencyId = tc.ID
                WHERE er.BaseCurrencyId = ? AND er.TargetCurrencyId = ?
                """,
                (base_currency_id, target_currency_id)
            )
            updated_row = cursor.fetchone()
            conn.close()
            return updated_row
        except sqlite3.Error as e:
            print(f"Database error in update_exchange_rate: {e}")
            raise


def get_exchange_rates_from_db(query, params=()):
    try:
        conn = sqlite3.connect('database/currency_exchange.db')
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise  # Проброс исключения наверх
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
