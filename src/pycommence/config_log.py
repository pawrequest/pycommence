import functools

from loguru import _logger

logger = None


# @functools.lru_cache(1)
# def configure_logging(logger_: _logger.Logger | None = None):
#     print(f'copnfiuguring logger with {logger_}')
#     global logger
#     if logger_:
#         logger = logger_
#         return
#     elif logger:
#         return
#     else:
#         from pawlogger import get_loguru
#
#         logger = get_loguru(profile='local', level='DEBUG')
