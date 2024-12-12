import json


class ResponseBuilder:
    @staticmethod
    def json_response(data: any, status: int = 200, content_type: str = 'application/json') -> tuple:
        """
        Формирует JSON-ответ для HTTP-запроса.

        :param data: Данные для включения в JSON-ответ.
        :param status: HTTP-статус ответа (по умолчанию 200).
        :param content_type: Заголовок Content-Type (по умолчанию 'application/json').
        :return: Кортеж (ответ в виде байтов, HTTP-статус, заголовок Content-Type).
        """
        try:
            response = json.dumps(data)
            return response.encode('utf-8'), status, content_type
        except (TypeError, ValueError) as e:
            print(f"Error serializing JSON response: {e}")
            raise

    @staticmethod
    def error_response(message: str, status: int = 500, content_type: str = 'application/json') -> tuple:
        """
        Формирует ошибочный JSON-ответ.

        :param message: Сообщение об ошибке.
        :param status: HTTP-статус ответа (по умолчанию 500).
        :param content_type: Заголовок Content-Type (по умолчанию 'application/json').
        :return: Кортеж (ответ в виде байтов, HTTP-статус, заголовок Content-Type).
        """
        return ResponseBuilder.json_response({'error': message}, status, content_type)
