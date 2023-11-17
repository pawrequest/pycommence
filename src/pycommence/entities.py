from dataclasses import dataclass


@dataclass
class Connection:
    name: str
    from_table: str
    to_table: str


class CmcError(Exception):
    def __init__(self, msg='Commence is not installed'):
        self.msg = msg
        super().__init__(self.msg)




