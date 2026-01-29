from dataclasses import dataclass
from functools import lru_cache

from pythoncom import COINIT_APARTMENTTHREADED, COINIT_MULTITHREADED


@dataclass
class Options:
    delim: str = ';*;%'
    application_name: str = 'Commence'
    application_db_name: str = 'Commence.DB'
    strip_strs: bool = False
    split_str_lists: bool = True
    max_cmd_len: int = 256  # undocumented Commence DDE cmd length limit
    fields_chunk: int = 12
    thread_model: int = COINIT_APARTMENTTHREADED


@lru_cache(maxsize=1)
def get_options():
    return Options()


__all__ = ['Options', 'get_options', 'COINIT_MULTITHREADED', 'COINIT_APARTMENTTHREADED']
