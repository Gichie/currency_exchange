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
            FROM ExchangeRates er
            JOIN Currencies bc ON er.BaseCurrencyId = bc.ID
            JOIN Currencies tc ON er.TargetCurrencyId = tc.ID
        """
        return get_exchange_ratesfrom_db(query)

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
                FROM ExchangeRates er
                JOIN Currencies bc ON er.BaseCurrencyId = bc.ID
                JOIN Currencies tc ON er.TargetCurrencyId = tc.ID
                WHERE bc.Code = ? AND tc.Code = ?
            """
        return get_exchange_ratesfrom_db(query, (base_currency_code, target_currency_code))


def get_exchange_ratesfrom_db(query, params=()):
    try:
        conn = sqlite3.connect('database/currency_exchange.db')
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        print(rows)
        return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise  # Проброс исключения наверх
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
