from pycommence.wrapper.cmc_cursor import CmcCursor
from pycommence.wrapper.cmc_entities import CmcError, Connection
from pycommence.wrapper.cmc_db import CmcDB

# def filter_by_date(
#         cursor: ICommenceCursor,
#         field_name: str,
#         date: datetime.date,
#         condition='After',
# ):
#     filter_str = f'[ViewFilter(1, F,, {field_name}, {condition}, {date})]'  # noqa E231
#     res = cursor.SetFilter(filter_str, 0)
#     return res

def filter_by_field(cursor: CmcCursor, field_name: str, condition, value=None, fslot=1):
    # filter_str = f'[ViewFilter(1, F,, "{field_name}", "{condition}", "{value})]'
    val_cond = f', "{value}"' if value else ''
    filter_str = f'[ViewFilter({fslot}, F,, {field_name}, {condition}{val_cond})]'  # noqa: E231
    res = cursor.set_filter(filter_str)
    return res


def filter_by_connection(cursor: CmcCursor, item_name: str, connection: Connection, fslot=1):
    filter_str = (f'[ViewFilter({fslot}, CTI,, {connection.desc}, '  # noqa: E231
                  f'{connection.to_table}, {item_name})]')
    res = cursor.set_filter(filter_str)
    if not res:
        raise ValueError(f'Could not set filter for ' f'{connection.desc} = {item_name}')
    #todo return


def filter_by_name(cursor: CmcCursor, name: str, fslot=1):
    res = filter_by_field(cursor, 'Name', 'Equal To', name, fslot=fslot)
    return res


def edit_record(cursor: CmcCursor, record, package: dict):
    filter_by_name(cursor, record)
    row_set = cursor.get_edit_row_set()
    for key, value in package.items():
        try:
            col_idx = row_set.get_column_index(key)
            row_set.modify_row(0, col_idx, str(value))
        except Exception:
            raise CmcError(f'Could not modify {key} to {value}')
    row_set.commit()
    ...


def get_record(cursor: CmcCursor, record_name):
    res = filter_by_name(cursor, record_name)
    if not res:
        raise CmcError(f'Could not find {record_name}')
    row_set = cursor.get_query_row_set()
    record = row_set.get_rows_dict()
    return record


def delete_record(cursor: CmcCursor, record_name):
    res = filter_by_name(cursor, record_name)
    row_set = cursor.get_delete_row_set()
    row_set.delete_row(0)
    res = row_set.commit()
    return res


def add_record(cursor: CmcCursor, record_name, package: dict):
    row_set = cursor.get_add_row_set(1)
    row_set.modify_row(0, 0, record_name)
    row_set.modify_row_dict(0, package)
    res = row_set.commit()
    return res

