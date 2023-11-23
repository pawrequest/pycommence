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

#
# def configure_logging(logger, log_file) -> logging.getLoggerClass():
#     # todo rotating file handler
#     # todo json output
#
#     logger.setLevel(logging.DEBUG)
#
#     file_handler = logging.FileHandler(log_file)
#     file_formatter = logging.Formatter('{levelname} {asctime} | {module}:{lineno} | {message}',
#                                        style='{')
#
#     file_handler.setFormatter(file_formatter)
#     logger.addHandler(file_handler)
#
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_formatter = logging.Formatter('{levelname} {message}', style='{')
#     console_handler.setFormatter(console_formatter)
#     console_handler.setLevel(logging.INFO)
#     logger.addHandler(console_handler)
#
#     return logger


