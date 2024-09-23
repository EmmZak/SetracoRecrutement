import logging


class Logger:
    def __init__(self, name: str) -> None:
        self.__logger = logging.getLogger(name)

    def _format_message(self, message, request=None):
        if request:
            return f"[User {request.user.username}] {message}"
        return message

    def debug(self, message, request=None):
        self.__logger.debug(self._format_message(message, request))

    def info(self, message, request=None):
        self.__logger.info(self._format_message(message, request))

    def warning(self, message, request=None):
        self.__logger.warning(self._format_message(message, request))

    def error(self, message, request=None):
        self.__logger.error(self._format_message(message, request))

    def critical(self, message, request=None):
        self.__logger.critical(self._format_message(message, request))
