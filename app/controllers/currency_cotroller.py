from app.services.currency_service import CurrencyService
from app.view import ResponseBuilder


class CurrencyController:
    @staticmethod
    def get_all_currencies():
        try:
            currencies = CurrencyService.get_all_currencies()
            return ResponseBuilder.json_response(currencies, status=200)
        except Exception as e:
            print(f"Error in CurrencyController.get_all_currencies: {e}")
            return ResponseBuilder.error_response("Internal Server Error", status=500)

    @staticmethod
    def get_currency(code):
        if not code:
            return ResponseBuilder.error_response("Currency code is missing", status=400)
        try:
            currency = CurrencyService.get_currency(code)
            if not currency:
                return ResponseBuilder.error_response("Currency not found", status=404)
            return ResponseBuilder.json_response(currency, status=200)
        except Exception as e:
            print(f"Error in CurrencyController.get_currency: {e}")
            return ResponseBuilder.error_response("Internal Server Error", status=500)

    @staticmethod
    def add_currency(data):
        required_fields = ["name", "code", "sign"]
        for field in required_fields:
            if field not in data or not data[field].strip():
                return ResponseBuilder.error_response(f"Missing required field: {field}", status=400)
        try:
            result = CurrencyService.add_currency(data["name"], data["code"], data["sign"])
            if result == "exists":
                return ResponseBuilder.error_response("Currency already exists", status=409)
            return ResponseBuilder.json_response({"message": "Currency added successfully"}, status=201)
        except Exception as e:
            print(f"Error in CurrencyController.add_currency: {e}")
            return ResponseBuilder.error_response("Internal Server Error", status=500)
