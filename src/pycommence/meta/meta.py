from abc import ABC
from typing import ClassVar, Optional, Self

from loguru import logger
from pydantic import BaseModel, model_validator

TABLE_TYPE_REGISTER: dict[str, type['CommenceTable']] = {}

TABLE_REGISTER: dict[str, 'CommenceTable'] = {}


def register_table_type(table_type: type['CommenceTable']) -> type['CommenceTable']:
    TABLE_TYPE_REGISTER[str(table_type.category)] = table_type
    logger.debug(f'Registered table model type: {table_type.category}')
    return table_type


def register_table(cls: type['CommenceTable']) -> 'CommenceTable':
    table = cls()
    TABLE_REGISTER[str(cls.category)] = table
    logger.debug(f'Registered table model: {cls.category}')
    return table


def get_table_type_model(table_name: str) -> type['CommenceTable'] | None:
    res = TABLE_TYPE_REGISTER.get(table_name)
    if not res:
        logger.warning(f'No table model found for csrname: {table_name}')
    return res


def get_table_model(table_name: str) -> Optional['CommenceTable']:
    res = TABLE_REGISTER.get(table_name)
    if not res:
        logger.warning(f'No table model found for csrname: {table_name}')
    return res


class CommenceTable(ABC, BaseModel):
    category: ClassVar[str]
    pk_key: ClassVar[str]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not getattr(cls, "category", None):
            raise TypeError(f"{cls.__name__} must define cetegory class variable")
        if not getattr(cls, "pk_key", None):
            raise TypeError(f"{cls.__name__} must define pk_key class variable")

        register_table(cls)


class CommenceRecord(BaseModel):
    table: CommenceTable
    data: dict[str, str]
    row_id: str | None = None
    row_pk_value: str | None = None

    @classmethod
    def from_dict(cls, table_name: str, data: dict):
        table_model = get_table_model(table_name)
        if not table_model:
            raise ValueError(f"No table model registered for table: {table_name}")
        return cls(table=table_model, data=data)

    @model_validator(mode='after')
    def id_or_pk(self) -> Self:
        if not self.row_id and not self.row_pk_value:
            pk_field = self.table.pk_key
            if pk_field not in self.data:
                raise ValueError(f"PK field '{pk_field}' not found in data to derive row_id")
            self.row_pk_value = self.data[pk_field]

        return self


class CommenceRecord2(BaseModel):
    table: CommenceTable
    data: dict[str, str]
