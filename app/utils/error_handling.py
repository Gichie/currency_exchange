import traceback
import logging
from app.views.response_builder import ResponseBuilder

# Настройка логирования
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(message)s")


class ErrorHandler:
    @staticmethod
    def log_exception(exc: Exception):
        """Логирует исключение с полным стек-трейсом."""
        logging.error(f"Exception occurred: {exc}")
        logging.error(traceback.format_exc())

    @staticmethod
    def handle_exception(exc: Exception):
        """Возвращает стандартный ответ на основе исключения."""
        ErrorHandler.log_exception(exc)
        return ResponseBuilder.error_response("Internal Server Error", status=500)