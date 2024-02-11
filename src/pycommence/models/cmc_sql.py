from abc import ABC
from typing import ClassVar

from sqlmodel import SQLModel

from pycommence.filters import FilterArray, CmcFilterPy
from pycommence.models.cmc_models import CmcModel


class CmcSql(SQLModel, CmcModel, ABC, table=True):
    ...

