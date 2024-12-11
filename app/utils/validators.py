class Validators:
    @staticmethod
    def is_valid_currency_code(code: str) -> bool:
        """
        Проверяет, что код валюты состоит из 3 буквенных символов.

        :param code: Код валюты (например, "USD").
        :return: True, если код корректен, иначе False.
        """
        return isinstance(code, str) and code.isalpha() and len(code) == 3

    @staticmethod
    def is_valid_rate(rate) -> float:
        """
        Проверяет, что курс обмена является положительным числом.

        :param rate: Курс обмена.
        :return: True, если курс положительный, иначе False.
        """
        try:
            return float(rate) > 0
        except ValueError:
            return False
