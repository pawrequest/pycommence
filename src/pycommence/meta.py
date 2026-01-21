from abc import ABC
from typing import ClassVar

from loguru import logger
from pydantic import BaseModel

from pycommence.pycmc_types import RowInfo

TABLE_REGISTER: dict[str, type['CommenceTable']] = {}


def register_table(cls: type['CommenceTable']) -> type['CommenceTable']:
    TABLE_REGISTER[str(cls.category)] = cls
    logger.debug(f'Registered table model: {cls.category}')
    return cls


def get_table_model(table_name: str) -> type['CommenceTable'] | None:
    res = TABLE_REGISTER.get(table_name)
    if not res:
        logger.warning(f'No table model found for csrname: {table_name}')
    return res


class CommenceTable(ABC, BaseModel):
    category: ClassVar[str]
    row_info: RowInfo

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not getattr(cls, "category", None):
            raise TypeError(f"{cls.__name__} must define a non-empty class attribute")

        register_table(cls)

