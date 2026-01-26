from abc import ABC
from typing import ClassVar, Self

from loguru import logger
from pydantic import BaseModel, ConfigDict, model_validator

TABLE_TYPE_REGISTER: dict[str, type['CommenceTable']] = {}


def register_table[T:type['CommenceTable']](cls: T) -> T:
    TABLE_TYPE_REGISTER[str(cls.category)] = cls
    logger.debug(f'Registered table model: {cls.category}')
    return cls


def get_table_type(table_name: str) -> type['CommenceTable'] | None:
    if res := TABLE_TYPE_REGISTER.get(table_name):
        return res
    raise ValueError(f'No table model found for csrname: {table_name}')


class CommenceTable(ABC, BaseModel):
    model_config = ConfigDict(extra='allow')
    category: ClassVar[str]
    pk_key: ClassVar[str]
    row_id: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not getattr(cls, "category", None):
            raise TypeError(f"{cls.__name__} must define cetegory class variable")
        if not getattr(cls, "pk_key", None):
            raise TypeError(f"{cls.__name__} must define pk_key class variable")

        register_table(cls)

