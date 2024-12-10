import sqlite3


class CurrencyRepository:
    @staticmethod
    def fetch_all():
        query = "SELECT * FROM currencies"
        return CurrencyRepository.execute_query(query)

    @staticmethod
    def fetch_by_code(code):
        query = "SELECT * FROM currencies WHERE code = ?"
        result = CurrencyRepository.execute_query(query, (code,))
        return result[0] if result else None


    @staticmethod
    def insert(name, code, sign):
        query = "INSERT INTO currencies (FullName, Code, Sign) VALUES (?, ?, ?)"
        return CurrencyRepository.execute_query(query, (name, code, sign))

    @staticmethod
    def execute_query(query, params=()):
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
