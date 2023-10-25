from dataclasses import dataclass
from enum import Enum


@dataclass
class Connector:
    desc: str
    key_table: str
    value_table: str



class CONNECTION(Enum):
    CUSTOMER_HIRES = Connector(key_table='Customer', desc="Has Hired", value_table='Hire')
    CUSTOMER_SALES = Connector(key_table='Customer', desc="Involves", value_table='Sale')
    HIRES_CUSTOMER = Connector(key_table='Hire', desc="To", value_table='Customer')
    SALES_CUSTOMER = Connector(key_table='Sale', desc="To", value_table='Customer')


class CmcError(Exception):
    ...