from typing import ContextManager, List

from .cmc_funcs import clean_dict, clean_hire_dict, connected_records_to_qs, get_cmc, qs_from_name, \
    qs_to_dicts
from .auto_cmc import ICommenceDB, ICommenceEditRowSet
from .cmc_entities import CONNECTION, CmcError


### functions to call


class CmcManager:
    def __init__(self, cmc_db):
        self.cmc_db = cmc_db


    def get_customer(self, record_name) -> dict:
        qs = qs_from_name(self.cmc_db, 'Customer', record_name)
        return clean_dict(qs_to_dicts(qs, 1)[0])


    def get_hire(self, record_name: str) -> dict:
        qs = qs_from_name(self.cmc_db, 'Hire', record_name)
        hire =  clean_hire_dict(qs_to_dicts(qs, 1)[0])
        qs2 = qs_from_name(self.cmc_db, 'Customer', hire['To Customer'])
        customer = clean_dict(qs_to_dicts(qs2, 1)[0])
        hire['customer'] = customer
        return hire


    def get_sale(self, record_name: str) -> dict:
        qs = qs_from_name(self.cmc_db, 'Sale', record_name)
        sale = clean_dict(qs_to_dicts(qs, 1)[0])
        qs2 = qs_from_name(self.cmc_db, 'Customer', sale['To Customer'])
        customer = clean_dict(qs_to_dicts(qs2, 1)[0])
        sale['customer'] = customer
        return sale

    def get_record_with_customer(self, table, record_name: str) -> dict:
        cleaner = clean_hire_dict if table == 'Hire' else clean_dict
        qs = qs_from_name(self.cmc_db, table, record_name)
        trans = cleaner(qs_to_dicts(qs, 1)[0])
        qs2 = qs_from_name(self.cmc_db, 'Customer', trans['To Customer'])
        customer = clean_dict(qs_to_dicts(qs2, 1)[0])
        trans['customer'] = customer
        return trans


    def sales_by_customer(self, customer_name: str, cmc=None) -> List[dict]:
        connection = CONNECTION.CUSTOMER_SALES
        qs = connected_records_to_qs(self.cmc_db, connection, customer_name)
        sales = qs_to_dicts(qs)
        for sale in sales:
            sale['customer'] = self.get_customer(sale['To Customer'])

        sales = [clean_dict(d) for d in sales]
        return sales


    def hires_by_customer(self, customer_name: str) -> List[dict]:
        connection = CONNECTION.HIRES_CUSTOMER
        recs = connected_records_to_qs(self.cmc_db, connection, customer_name)
        hires = qs_to_dicts(recs)
        for hire in hires:
            hire['customer'] = self.get_customer(hire['To Customer'])
        hires = [clean_hire_dict(d) for d in hires]
        return hires

    def edit_record(self, table, hire_name, package: dict):
        edit_set: ICommenceEditRowSet = qs_from_name(self.cmc_db, table, hire_name, edit=True)
        for key, value in package.items():
            try:
                col_idx = edit_set.GetColumnIndex(key, 0)
                edit_set.ModifyRow(0, col_idx, str(value), 0)
            except:
                raise CmcError(f"Could not modify {key} to {value}")
        edit_set.Commit(0)
        ...



class CmcContext(ContextManager):
    def __init__(self, cmc_db: ICommenceDB = None):
        self.cmc_db = cmc_db or get_cmc()

    def __enter__(self) -> CmcManager:
        return CmcManager(self.cmc_db)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cmc_db = None

