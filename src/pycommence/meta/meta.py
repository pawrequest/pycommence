from abc import ABC
from typing import ClassVar, Self

from loguru import logger
from pydantic import BaseModel, model_validator

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


class Contact(CommenceTable):
    category: ClassVar[str] = "Contact"
    pk_key: ClassVar[str] = "contactKey"


class CommenceRecord(BaseModel):
    category: str
    data: dict[str, str]
    row_id: str | None = None
    row_pk_value: str | None = None

    # table_model: type = None

    @classmethod
    def from_dict(cls, table_name: str, data: dict):
        table_model_type = get_table_type(table_name)
        if not table_model_type:
            raise ValueError(f"No table model registered for table type: {table_name} in {TABLE_TYPE_REGISTER=}")
        return cls(data=data, category=table_model_type.category)

    @model_validator(mode='after')
    def id_or_pk(self) -> Self:
        if not self.row_id and not self.row_pk_value:
            table_model = get_table_type(self.category)
            if not table_model:
                raise ValueError(f"No table model registered for table type: {self.category} in {TABLE_TYPE_REGISTER=}")
            pk_field = table_model.pk_key
            if pk_field not in self.data:
                raise ValueError(f"PK field '{pk_field}' not found in data to derive row_id")
            self.row_pk_value = self.data[pk_field]

        return self
