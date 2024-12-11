import json


class ResponseBuilder:
    @staticmethod
    def json_response(data, status=200, content_type='application/json'):
        """Формирует JSON-ответ для HTTP-запроса."""
        try:
            response = json.dumps(data)
            return response.encode('utf-8'), status, content_type
        except (TypeError, ValueError) as e:
            print(f"Error serializing JSON response: {e}")
            raise

    @staticmethod
    def error_response(message, status=500, content_type='application/json'):
        """Формирует ошибочный ответ."""
        return ResponseBuilder.json_response({'error': message}, status, content_type)
