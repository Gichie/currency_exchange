import sqlite3


class ExchangeRateRepository:
    @staticmethod
    def fetch_all():
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
    def fetch_by_pair(base_currency_code, target_currency_code):
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
    def insert(base_currency_id, target_currency_id, rate):
        query = """
            INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate)
            VALUES (?, ?, ?)
        """
        return ExchangeRateRepository.execute_query(query, (base_currency_id, target_currency_id, rate))

    @staticmethod
    def update(base_currency_id, target_currency_id, rate):
        query = """
            UPDATE ExchangeRates
            SET Rate = ?
            WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?
        """
        return ExchangeRateRepository.execute_query(query, (rate, base_currency_id, target_currency_id))

    @staticmethod
    def execute_query(query, params=()):
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
