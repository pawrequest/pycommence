from dataclasses import dataclass


@dataclass
class Connector:
    desc: str
    from_table: str
    to_table: str


CUSTOMER_HIRES_CTI = Connector(from_table='Customer', desc='Has Hired', to_table='Hire')
CUSTOMER_SALES_CTI = Connector(from_table='Customer', desc='Involves', to_table='Sale')
HIRES_CUSTOMER_CTI = Connector(from_table='Hire', desc='To', to_table='Customer')
SALES_CUSTOMER_CTI = Connector(from_table='Sale', desc='To', to_table='Customer')


class CmcError(Exception):
    ...


class CommenceNotInstalled(Exception):
    def __init__(self, msg='Commence is not installed'):
        self.msg = msg
        super().__init__(self.msg)
