# pycommence

python wrapper for Commence RM 8.0

pywin32 for com-object interactions

makepy file for object definitions

python api to connect to and create update and remove from the database


# usage:

* instantiate db connection:
    `db = CmcDB()`

* instantiate cursor: 
    `cursor = db.get_cursor('Hire')`

* better yet use `pycommence/csr_api.py.get_csr` and let internals handle the db connection

## CSR convenience methods
    - `edit_record(name: str, package: dict) -> None`
    - `get_record(record_name: str) -> dict[str, str]`
    - `get_all_records() -> list[dict[str, str]]`
    - `delete_record(record_name)`
    - 'add_record(record_name: str, package: dict) -> bool'
    - 


    `
- 

    



  
  
```