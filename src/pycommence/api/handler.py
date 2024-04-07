import pydantic as _p

from pycommence.api import CmcError, csr_api


class CmcHandler(_p.BaseModel):
    """
    handle cursors to retrieve data with different filter configurations
    """
    db_name: str = 'Commence.db'
    table: str

    def check_exists_pk(self, pk_val: str) -> bool:
        with csr_api.csr_context(self.table) as csr:
            try:
                csr.filter_by_pk(pk_val)
                return True
            except CmcError as e:
                if 'No record found for ' in e.msg:
                    return False
                raise

    def records_by_field(self, field_name: str, value: str, max_rtn=None) -> list[dict[str, str]]:
        with csr_api.csr_context(self.table) as csr:
            return csr.records_by_field(field_name, value, max_rtn)

    def record_by_name(self, name: str) -> dict[str, str]:
        return self.records_by_field('Name', name, 1)[0]

    def add_record(self, package: dict[str, str]):
        with csr_api.csr_context(self.table) as csr:
            ...

    def col0(self):
        with csr_api.csr_context(self.table) as csr:
            ...
