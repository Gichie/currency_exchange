from app.models.exchange_rate_model import ExchangeRateModel


class ExchangeRateService:
    @staticmethod
    def format_exchange_rate(row):
        return {
            "id": row[0],
            "base_currency": {
                "id": row[1],
                "code": row[2],
                "name": row[3],
                "sign": row[4]
            },
            "target_currency": {
                "id": row[5],
                "name": row[6],
                "code": row[7],
                "sign": row[8]
            },
            "rate": row[9]
        }

    @staticmethod
    def get_all_exchange_rates():
        rows = ExchangeRateModel.get_all_exchange_rates()
        return [ExchangeRateService.format_exchange_rate(row) for row in rows]

    @staticmethod
    def get_exchange_rate_by_pair(base_currency_code, target_currency_code):
        rows = ExchangeRateModel.get_exchange_rate_by_pair(base_currency_code, target_currency_code)
        if not rows:
            return None
        return ExchangeRateService.format_exchange_rate(rows[0])
