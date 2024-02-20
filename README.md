# **pycommence** - A python wrapper for Commence RM 8.0

- pydantic for safety
- pywin32 for com-object interactions
- makepy file for object definitions

## Usage

`pycommence/csr_api.py.get_csr` returns a `Csr` object - the primary API class with methods for interacting with the
Commence database.

## Types

### Enums

- `FilterTypeEnum(StrEnum)` - enum for filter types
- `NotFlag(StrEnum)` - enum for not flag
- `FilterCondition(StrEnum)` - enum for filter conditions

### Wrappers

- `cmc_db.Cmc(CmcConnection)` - thin wrapper on the Commence DB object
- `cmc_cursor.CsrCmc` - thin wrapper on the Commence Cursor object

### API

- `cmc_db.py.CmcConnection` - singleton connector to Commence databases
- `cmc_cursor.Csr` - primary API
- `filters.CmcFilter` - filter object 
- `filters.FilterArray` - array of filters



## CSR convenience methods

- `edit_record(name: str, package: dict) -> None`
- `get_record(record_name: str) -> dict[str, str]`
- `get_all_records() -> list[dict[str, str]]`
- `delete_record(record_name)`
- `add_record(record_name: str, package: dict) -> bool`
- `filter_by_array(self, fil_array: FilterArray, get_all=False) -> None | list[dict[str, str]]`
- 