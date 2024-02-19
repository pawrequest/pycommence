from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from pydantic import BaseModel, ValidationError

from pycommence import get_csr
from pycommence.models import CmcModel
from pycommence.models.cmc_models import CmcTableRaw


class CmcTableRawSql(SQLModel, ABC):
    table_name: ClassVar[str]

    class Config:
        extra = 'ignore'


class CmcModelSql(SQLModel, ABC):
    # initial_filter_array: ClassVar[None | list[CmcFilterPy]] = None
    cmc_class: ClassVar[type[CmcTableRaw]]

    @classmethod
    @abstractmethod
    def from_cmc(cls, cmc_obj: BaseModel) -> CmcModel:
        raise NotImplementedError

    @classmethod
    def from_name(cls, name: str) -> CmcModel:
        csr = get_csr(cls.cmc_class.table_name)
        record = csr.get_record(name)
        cmc = cls.cmc_class(**record)
        return cls.from_cmc(cmc)

    @classmethod
    def from_record(cls, record: dict[str, str]) -> CmcModel:
        try:
            cmc = cls.cmc_class(**record)
            return cls.from_cmc(cmc)
        except ValidationError as e:
            raise ValueError(f'Failed to convert record to {cls.__name__}') from e
