class Validators:
    @staticmethod
    def is_valid_currency_code(code: str):
        """Проверяет, что код валюты состоит из 3 буквенных символов."""
        return isinstance(code, str) and code.isalpha() and len(code) == 3

    @staticmethod
    def is_valid_rate(rate):
        """Проверяет, что курс обмена — положительное число."""
        try:
            return float(rate) > 0
        except ValueError:
            return False