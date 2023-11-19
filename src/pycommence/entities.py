import json
import logging
import sys
from dataclasses import dataclass

FLAGS_UNUSED = 0


@dataclass
class Connection:
    name: str
    from_table: str
    to_table: str


class CmcError(Exception):
    def __init__(self, msg='Commence is not installed'):
        self.msg = msg
        super().__init__(self.msg)


class NotFoundError(Exception):
    def __init__(self, msg='No records found'):
        self.msg = msg
        super().__init__(self.msg)




class JSONFormatter(logging.Formatter):
    def format(self, record):
        # Call the base class's format method
        formatted_message = super().format(record)
        # super().format(record)

        # Convert the formatted string to a JSON object
        # You might need to adjust this part based on how you want the JSON to be structured
        log_record = {
            "asctime": record.asctime,
            "levelname": record.levelname,
            "module": record.module,
            "lineno": record.lineno,
            "message": record.msg,
        }

        return json.dumps(log_record)


def configure_logging(log_file):
    # todo rotating file handler
    # todo json output
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter('{levelname} {asctime} | {module}:{lineno} | {message}', style='{')

    file_formatter = JSONFormatter()
    file_formatter.usesTime()

    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter('{levelname} {message}', style='{')
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
