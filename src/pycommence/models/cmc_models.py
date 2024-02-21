from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from pydantic import BaseModel, ValidationError
from sqlmodel import SQLModel

from pycommence import get_csr
from pycommence.filters import CmcFilter


def sub_model_from_cmc[T](
        cls: type[T],
        cmc_obj: CmcTableRaw | CmcModel,
        *,
        prepend: str = ''
) -> T:
    ob_dict = {
        attr: getattr(cmc_obj, f'{prepend}{attr}') for attr in cls.model_fields
    }
    return cls.model_validate(ob_dict)


class CmcTableRaw(SQLModel, ABC):
    table_name: ClassVar[str]

    class Config:
        extra = 'ignore'


class CmcModel(SQLModel, ABC):
    cmc_class: ClassVar[type[CmcTableRaw]]
    initial_filter_array: ClassVar[list[CmcFilter] | None] = None

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
