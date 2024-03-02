from datetime import datetime

from .api.cmc_csr import Csr, get_csr, csr_context
from .api.cmc_db import Cmc
from .api.cmc_types import CmcFilter, FilterArray, FilterConditionType, Connection
from .wrapper.cmc_enums import OptionFlag


CmcDateFormat = '%Y%m%d'
CmcTimeFormat = '%H:%M'


def get_cmc_date(datestr: str):
    """ Use CMC Cannonical flag"""
    return datetime.strptime(datestr, CmcDateFormat).date()


def get_cmc_time(time_str: str):
    """ Use CMC Cannonical flag"""
    return datetime.strptime(time_str, CmcTimeFormat).time()
__all__ = [
    "Cmc",
    "Csr",
    "CmcFilter",
    "FilterArray",
    "get_csr",
    "csr_context",
    "FilterConditionType",
    "Connection",
    "OptionFlag",
    "get_cmc_date",
    "get_cmc_time",
    "CmcDateFormat",
    "CmcTimeFormat",
]