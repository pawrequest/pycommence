from __future__ import annotations

from abc import ABC
from typing import ClassVar

from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass

from pycommence.api.api_types import CmcFilter


# def sub_model_from_cmc(cls, cmc_obj, *, prepend: str = ''):
#     ob_dict = {}
#     for attr, field in cls.__fields__.items():
#         full_attr_name = f'{prepend}{attr}' if prepend else attr
#         if issubclass(field.type_, BaseModel):
#             nested_model_cls = field.type_
#             nested_prepend = f'{full_attr_name}.' if prepend else f'{attr}.'
#             res = sub_model_from_cmc(nested_model_cls, cmc_obj, prepend=nested_prepend)
#         else:
#             res = getattr(cmc_obj, full_attr_name, None)
#         ob_dict[attr] = res
#     return cls(**ob_dict)

#
def sub_model_from_cmc[T](
        cls: type[T],
        cmc_obj,
        *,
        prepend: str = ''
) -> T:
    ob_dict = {}
    for attr in cls.model_fields:
        full_attr_name = f'{prepend}{attr}'
        # sub_info = cls.model_fields[full_attr_name].annotation.model_fields
        if isinstance(cls.model_fields[full_attr_name].annotation, ModelMetaclass):
            nested_model_cls = cls.model_fields[full_attr_name].annotation
            # nested_prepend = f'{full_attr_name}'
            res = sub_model_from_cmc(nested_model_cls, cmc_obj)
        else:
            res = getattr(cmc_obj, full_attr_name, None)
        ob_dict[full_attr_name] = res
    return cls.model_validate(ob_dict)

    # ob_dict = {
    #     attr: getattr(cmc_obj, f'{prepend}{attr}') for attr in cls.model_fields if
    #     hasattr(cmc_obj, f'{prepend}{attr}')
    # }


class CmcModel(BaseModel, ABC):
    cmc_table_name: ClassVar[str]
    record: dict[str, str]
    initial_filter_array: ClassVar[list[CmcFilter] | None] = None

    # @classmethod
    # def from_name(cls, name: str) -> CmcModelIn:
    #     csr = get_csr(cls.raw_table_class.cmc_table_name)
    #     record = csr.get_record(name)
    #     cmc = cls.raw_table_class(**record, record=record)
    #     return cls.from_raw_cmc(cmc)
    #
    # @classmethod
    # def from_namedb(cls, name: str, session) -> CmcModelIn:
    #     if not hasattr(cls, 'from_raw'):
    #         raise NotImplementedError
    #     csr = get_csr(cls.raw_table_class.cmc_table_name)
    #     record = csr.get_record(name)
    #     cmc = cls.raw_table_class(**record, record=record)
    #     return cls.from_raw(cmc, session)
    #
    # @classmethod
    # def from_record(cls, record: dict[str, str]) -> CmcModelIn:
    #     try:
    #         cmc = cls.raw_table_class(**record, record=record)
    #         return cls.from_raw_cmc(cmc)
    #     except ValidationError as e:
    #         raise ValueError(f'Failed to convert record to {cls.__name__}') from e
    #
