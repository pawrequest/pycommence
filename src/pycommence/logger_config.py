import inspect
import logging

CONSOLE_FORMAT_STR = '{levelname} - {module}:{lineno} - {message}'
FILE_FORMAT_STR = '{levelname} - {asctime} - {module}:{lineno} - {message}'


def configure_logging(log_file, level=logging.DEBUG):
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    module_name = module.__name__ if module else '__main__'

    logger = logging.getLogger(module_name)
    logger.setLevel(level)

    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    file_formatter = logging.Formatter(FILE_FORMAT_STR, style='{')
    console_formatter = logging.Formatter(CONSOLE_FORMAT_STR, style='{')

    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


