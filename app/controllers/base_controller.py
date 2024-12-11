from typing import Optional

from app.views.response_builder import ResponseBuilder


class BaseController:
    @staticmethod
    def handle_exceptions(func):
        """
        Декоратор для обработки исключений в методах контроллеров.
        Если возникает ошибка, возвращает стандартный ответ с кодом 500.

        :param func: Функция контроллера, обёрнутая декоратором.
        :return: Результат выполнения функции или JSON-ответ с ошибкой.
        """

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Unhandled exception in controller: {e}")
                return ResponseBuilder.error_response("Internal Server Error", status=500)

        return wrapper

    @staticmethod
    def validate_required_fields(data: dict, required_fields: list[str]) -> Optional[dict]:
        """
        Проверяет, что в данных присутствуют все обязательные поля.

        :param data: Словарь с данными.
        :param required_fields: Список обязательных полей.
        :return: None, если все поля есть, иначе JSON-ответ с ошибкой.
        """
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return ResponseBuilder.error_response(
                f"Missing required fields: {', '.join(missing_fields)}", status=400
            )
        return None
