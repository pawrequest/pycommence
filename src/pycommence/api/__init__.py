from __future__ import annotations

import contextlib

from .cmc_csr import Csr
from .cmc_db import Cmc
from .filters import CmcFilter, FilterArray
from .entities import CmcError
from ..wrapper import Bookmark, CursorType, OptionFlag


@contextlib.contextmanager
def csr_cm(table_name, cmc_name: str = 'Commence.DB') -> Csr:
    """Context manager for a cursor object."""
    cmc = Cmc(cmc_name)
    csr = cmc.get_cursor(table_name)
    try:
        yield csr
    finally:
        ...


def get_csr(table_name, cmc_name: str = 'Commence.DB') -> Csr:
    """ Easiest entry - Get a cursor for a table in a Commence database."""
    cmc = Cmc(cmc_name)
    return cmc.get_cursor(table_name)


__all__ = ['Cmc', 'Csr', 'csr_cm', 'get_csr', 'CmcError', 'CmcFilter', 'FilterArray', 'CursorType',
           'OptionFlag', 'Bookmark']
