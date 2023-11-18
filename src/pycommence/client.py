from win32com.client import Dispatch
""" maybe cache cursors or smth?"""

# class CmcHandler:
#     _db = None
#     _csrs = {}
#     _db_name = "Commence.DB"
#
#     def __new__(cls, table_name):
#         # retrieve or get db connection
#         cls._db = cls._db or Dispatch(cls._db_name)
#
#
#         # retrieve or get cursor
#         csr1 = cls._csrs.get(table_name, cls._db.GetCursor(table_name))
#         if (csr := cls._csrs.get(table_name)) is not None:
#             print(f'returning existing cursor {table_name} from cache')
#             return csr
#         csr = super().__new__(cls)
#         cls._csrs[table_name] = csr
#         csr._connect(cls)
#         return csr
#


class Client:
    _loaded = {}
    _db_file = "file.db"

    def __new__(cls, client_id):
        if (client := cls._loaded.get(client_id)) is not None:
            print(f'returning existing client {client_id} from cache')
            return client
        client = super().__new__(cls)
        cls._loaded[client_id] = client
        client._init_from_file(client_id, cls._db_file)
        return client

    def _init_from_file(self, client_id, file):
        # lookup client in file and read properties
        print(f'reading client {client_id} data from file, db, etc.')
        name = ...
        email = ...
        self.name = name
        self.email = email
        self.id = client_id


def cached_clients_example():
    print("CLIENT CACHE EXAMPLE")
    x = Client(0)
    y = Client(0)
    print(f'{x is y=}')
    z = Client(1)
