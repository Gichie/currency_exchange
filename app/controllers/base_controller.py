from app.views.response_builder import ResponseBuilder


class BaseController:
    @staticmethod
    def handle_exceptions(func):
        """
        Декоратор для обработки исключений в методах контроллеров.
        Если возникает ошибка, возвращает стандартный ответ с кодом 500.
        """

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Unhandled exception in controller: {e}")
                return ResponseBuilder.error_response("Internal Server Error", status=500)

        return wrapper

    @staticmethod
    def validate_required_fields(data, required_fields):
        """
        Проверяет, что в данных присутствуют все обязательные поля.
        Возвращает None, если все поля есть, иначе JSON-ответ с ошибкой.
        """
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return ResponseBuilder.error_response(
                f"Missing required fields: {', '.join(missing_fields)}", status=400
            )
        return None
