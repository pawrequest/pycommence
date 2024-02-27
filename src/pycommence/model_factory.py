from pycommence.api import csr_context
from pycommence.cmc_models import CmcModel

#
# def from_name(table, name: str) -> CmcModel:
#     with csr_context(table) as csr:
#         record = csr.get_record(name)
#     cmc = CmcModel(record=record)
#     cmc = cls.raw_table_class(**record, record=record)
#     return cls.from_raw_cmc(cmc)
#
#
# @classmethod
# def from_namedb(cls, name: str, session) -> CmcModel:
#     if not hasattr(cls, 'from_raw'):
#         raise NotImplementedError
#     csr = get_csr(cls.raw_table_class.cmc_table_name)
#     record = csr.get_record(name)
#     cmc = cls.raw_table_class(**record, record=record)
#     return cls.from_raw(cmc, session)
#
#
# @classmethod
# def from_record(cls, record: dict[str, str]) -> CmcModel:
#     try:
#         cmc = cls.raw_table_class(**record, record=record)
#         return cls.from_raw_cmc(cmc)
#     except ValidationError as e:
#         raise ValueError(f'Failed to convert record to {cls.__name__}') from e
#
