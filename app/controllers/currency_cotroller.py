from app.controllers.base_controller import BaseController
from app.services.currency_service import CurrencyService
from app.views.response_builder import ResponseBuilder


class CurrencyController:
    @staticmethod
    @BaseController.handle_exceptions
    def add_currency(data):
        """Добавляет новую валюту."""
        required_fields = ["name", "code", "sign"]
        validation_error = BaseController.validate_required_fields(data, required_fields)
        if validation_error:
            return validation_error  # Возвращает ошибку, если поля отсутствуют

        response, status = CurrencyService.add_currency(data)
        return ResponseBuilder.json_response(response, status=status)

    @staticmethod
    def home():
        """Возвращает приветственное сообщение."""
        return ResponseBuilder.json_response({"message": "Welcome to the Currency Exchange API!"}, status=200)

    @staticmethod
    def get_all_currencies():
        """Получает список всех валют."""
        try:
            currencies = CurrencyService.get_all_currencies()
            return ResponseBuilder.json_response(currencies, status=200)
        except Exception as e:
            print(f"Error in CurrencyController.get_all_currencies: {e}")
            return ResponseBuilder.error_response("Internal Server Error", status=500)

    @staticmethod
    def get_currency(code):
        """Получает информацию о валюте по коду."""
        if not code:
            return ResponseBuilder.error_response("Currency code is missing", status=400)

        try:
            currency = CurrencyService.get_currency_by_code(code.upper())
            if not currency:
                return ResponseBuilder.error_response("Currency not found", status=404)
            return ResponseBuilder.json_response(currency, status=200)
        except Exception as e:
            print(f"Error in CurrencyController.get_currency: {e}")
            return ResponseBuilder.error_response("Internal Server Error", status=500)

    @staticmethod
    def add_currency(data):
        """Добавляет новую валюту."""
        required_fields = ["name", "code", "sign"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return ResponseBuilder.error_response(
                f"Missing required fields: {', '.join(missing_fields)}", status=400
            )

        try:
            response, status = CurrencyService.add_currency(data)
            return ResponseBuilder.json_response(response, status=status)
        except Exception as e:
            print(f"Error in CurrencyController.add_currency: {e}")
            return ResponseBuilder.error_response("Internal Server Error", status=500)
