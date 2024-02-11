from typing import Optional

from pydantic import BaseModel, Field

from amherst.models.shared import CmcTable
from pawsupport.convert import to_snake
from pycommence import CsrCmc
from pycommence.wrapper.cmc_db import get_csr


# class CmcMeta(type):
#     def __new__(cls, name, bases, dct):
#         if 'CmcTable' in [base.__name__ for base in bases]:
#             if 'table_name' not in dct:
#                 dct['table_name'] = name  # Or some transformation of name
#         return super().__new__(cls, name, bases, dct)
#
#     def __init__(cls, name, bases, dct):
#         super().__init__(name, bases, dct)
#         if 'CmcConverted' in [base.__name__ for base in bases]:
#             cls.cmc_class = globals().get(f"{name.replace('Converted', '')}Cmc")
#             if cls.cmc_class is None:
#                 raise ValueError(f"Corresponding CmcTable class for {name} not found")
#
#
# class CmcTable(metaclass=CmcMeta):
#     pass
#
#
# class CmcConverted(BaseModel, metaclass=CmcMeta):
#     @classmethod
#     @abstractmethod
#     def from_cmc(cls, cmc_obj: BaseModel) -> 'CmcConverted':
#         raise NotImplementedError
#

# class HireCmc(CmcTable):
#     ...
#     # Class definition remains the same
#
#
# class Hire(CmcConverted):
#     ...
#     # Now, you don't need to explicitly set cmc_class
#     # The rest of the class definition remains the same


def get_table_schema(table_name):
    csr: CsrCmc = get_csr(table_name)
    # This function is just a placeholder.
    # You would replace it with the actual code to query your database schema.
    # For example, it might return [('id', 'INTEGER'), ('name', 'VARCHAR'), ...]
    return [('name', 'VARCHAR'), ('reference_number', 'VARCHAR')]


def create_pydantic_model_from_db(table_name):
    csr = get_csr(table_name)
    schema = csr.get_schema
    attributes = {
        '__annotations__': {},
    }

    for column_name, column_type in schema.items():
        alias, column_name = column_name, to_snake(column_name)
        attributes['__annotations__'][column_name] = column_type

        attributes[column_name] = Field(alias=alias)

    # Create the Pydantic model class dynamically
    model_class = type(table_name, (CmcTable,), attributes)

    return model_class
