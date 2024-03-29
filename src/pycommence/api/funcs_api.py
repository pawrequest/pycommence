from win32com.universal import com_error

from pycommence.api import types_api
from pycommence.wrapper.cursor import CsrCmc
"""
Functional approach to creating an API, mostly unused in favor of the ORM.
"""

def filter_by_field(cursor: CsrCmc, field_name: str, condition, value=None, fslot=1):
    val_cond = f', "{value}"' if value else ''
    filter_str = f'[ViewFilter({fslot}, F,, {field_name}, {condition}{val_cond})]'  # noqa: E231
    res = cursor.set_filter(filter_str)
    return res


def filter_by_connection(cursor: CsrCmc, item_name: str, connection: cmc_types.Connection, fslot=1):
    filter_str = (f'[ViewFilter({fslot}, CTI,, {connection.name}, '  # noqa: E231
                  f'{connection.to_table}, {item_name})]')
    res = cursor.set_filter(filter_str)
    if not res:
        raise ValueError(f'Could not set filter for ' f'{connection.name} = {item_name}')
    # todo return


def filter_by_name(cursor: CsrCmc, name: str, fslot=1):
    res = filter_by_field(cursor, 'Name', 'Equal To', name, fslot=fslot)
    return res


def edit_record(cursor: CsrCmc, record, package: dict):
    filter_by_name(cursor, record)
    row_set = cursor.get_edit_row_set()
    for key, value in package.items():
        try:
            col_idx = row_set.get_column_index(key)
            row_set.modify_row(0, col_idx, str(value))
        except Exception:
            raise cmc_types.CmcError(f'Could not modify {key} to {value}')
    row_set.commit()
    ...


def get_all_records(cursor: CsrCmc) -> list[dict[str, str]]:
    qs = cursor.get_query_row_set()
    return qs.get_rows_dict()


def get_record(cursor: CsrCmc, record_name):
    res = filter_by_name(cursor, record_name)
    if not res:
        raise cmc_types.CmcError(f'Could not find {record_name}')
    row_set = cursor.get_query_row_set()
    record = row_set.get_rows_dict()[0]
    return record


def delete_record(cursor: CsrCmc, record_name):
    try:
        filter_by_name(cursor, record_name)
        row_set = cursor.get_delete_row_set()
        row_set.delete_row(0)
        res = row_set.commit()
        return res
    except Exception:
        ...


def add_record(cursor: CsrCmc, record_name, package: dict):
    try:
        row_set = cursor.get_add_row_set(1)
        row_set.modify_row(0, 0, record_name)
        row_set.modify_row_dict(0, package)
        res = row_set.commit()
        return res

    except com_error as e:
        # todo this is horrible. the error is due to threading but we are not using threading?
        # maybe pywin32 uses threading when handling the underlying db error?
        if e.hresult == -2147483617:
            raise cmc_types.CmcError('Record already exists')
