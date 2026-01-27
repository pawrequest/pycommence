from enum import StrEnum
from collections.abc import Sequence

from pycommence.dde_generators.dde_msg import _dde_format_function
from pycommence.meta.pycmc_fields import DELIM


def dde_view_category(category: str) -> str:
    return _dde_format_function('ViewCategory', [category])


def dde_view_conjunction(
        and_or_12: str | None = None,
        and_or_13: str | None = None,
        and_or_34: str | None = None
) -> str:
    return _dde_format_function('ViewConjunction', [and_or_12, and_or_13, and_or_34])


def dde_view_filter(
        clause_number: int,
        filter_type: str,
        not_flag: str | None,
        *filter_type_parameters: str | None
) -> str:
    """
    Docs: ViewFilter(ClauseNumber, FilterType, NotFlag, FieldTypeParameters...)
    not_flag must be present positionally; pass None for blank placeholder.
    """
    return _dde_format_function('ViewFilter', [clause_number, filter_type, not_flag, *filter_type_parameters])


def dde_view_sort(*field_sort_pairs: str) -> str:
    """
    Docs: ViewSort(Field1, Sort1, Field2, Sort2, Field3, Sort3, Field4, Sort4)
    Pass as: field1, sort1, field2, sort2, ...
    """
    if (len(field_sort_pairs) % 2) != 0:
        raise ValueError('ViewSort requires even args: Field, Sort pairs.')
    if len(field_sort_pairs) > 8:
        raise ValueError('ViewSort supports up to 4 Field/Sort pairs (8 args).')
    return _dde_format_function('ViewSort', list(field_sort_pairs))


def dde_view_view(view_name: str | None = None) -> str:
    return _dde_format_function('ViewView', [view_name])


def dde_view_item_count() -> str:
    return _dde_format_function('ViewItemCount', [])


def dde_view_field(index: int, field: str) -> str:
    return _dde_format_function('ViewField', [index, field])


def dde_view_fields(index: int, fields: Sequence[str], delim: str = DELIM) -> str:
    # fields = fields[:-2]
    n = len(fields)
    return _dde_format_function('ViewFields', [index, n, *fields, delim])


def dde_view_item_name(index: int) -> str:
    return _dde_format_function('ViewItemName', [index])


def dde_view_item_index(name_field_value: str | None = None) -> str:
    return _dde_format_function('ViewItemIndex', [name_field_value])


def dde_view_connected_count(index: int, connection_name: str, to_category: str) -> str:
    return _dde_format_function('ViewConnectedCount', [index, connection_name, to_category])


def dde_view_connected_item(index: int, connection_name: str, to_category: str, conn_index: int) -> str:
    return _dde_format_function('ViewConnectedItem', [index, connection_name, to_category, conn_index])


def dde_view_connected_field(index: int, connection_name: str, to_category: str, conn_index: int, field: str) -> str:
    return _dde_format_function('ViewConnectedField', [index, connection_name, to_category, conn_index, field])


def dde_view_connected_fields(
        index: int,
        connection_name: str,
        to_category: str,
        conn_index: int,
        fields: Sequence[str],
        delim: str | None = None
) -> str:
    n = len(fields)
    return _dde_format_function(
        'ViewConnectedFields',
        [index, connection_name, to_category, conn_index, n, *fields, delim]
    )


def dde_view_mark_item(index: int) -> str:
    return _dde_format_function('ViewMarkItem', [index])


def dde_view_delete_all_items() -> str:
    return _dde_format_function('ViewDeleteAllItems', [])


def dde_view_field_to_file(index: int, field: str, filename: str) -> str:
    return _dde_format_function('ViewFieldToFile', [index, field, filename])


def dde_view_image_field_to_file(index: int, field: str, filename: str) -> str:
    return _dde_format_function('ViewImageFieldToFile', [index, field, filename])


def dde_view_save_view(new_view_name: str, shared: str | None = None) -> str:
    """
    Docs: shared is "yes" or "no"
    """
    return _dde_format_function('ViewSaveView', [new_view_name, shared])


class DDECmdView(StrEnum):
    CATEGORY = 'ViewCategory'
    CONJUNCTION = 'ViewConjunction'
    FILTER = 'ViewFilter'
    SORT = 'ViewSort'
    VIEW = 'ViewView'
    ITEM_COUNT = 'ViewItemCount'
    FIELD = 'ViewField'
    FIELDS = 'ViewFields'
    ITEM_NAME = 'ViewItemName'
    ITEM_INDEX = 'ViewItemIndex'
    CONNECTED_COUNT = 'ViewConnectedCount'
    CONNECTED_ITEM = 'ViewConnectedItem'
    CONNECTED_FIELD = 'ViewConnectedField'
    CONNECTED_FIELDS = 'ViewConnectedFields'
    MARK_ITEM = 'ViewMarkItem'
    DELETE_ALL_ITEMS = 'ViewDeleteAllItems'
    FIELD_TO_FILE = 'ViewFieldToFile'
    IMAGE_FIELD_TO_FILE = 'ViewImageFieldToFile'
    SAVE_VIEW = 'ViewSaveView'