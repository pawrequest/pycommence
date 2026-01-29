from collections.abc import Sequence

from pycommence.dde.types import DDERequestView
from pycommence.core.fields import DELIM


def view_category(category: str) -> DDERequestView:
    return DDERequestView(func_name='ViewCategory', params=[category])


def view_conjunction(
        and_or_12: str | None = None,
        and_or_13: str | None = None,
        and_or_34: str | None = None
) -> DDERequestView:
    return DDERequestView(func_name='ViewConjunction', params=[and_or_12, and_or_13, and_or_34])


def view_filter(
        clause_number: int,
        filter_type: str,
        not_flag: str | None,
        *filter_type_parameters: str | None
) -> DDERequestView:
    """
    Docs: ViewFilter(ClauseNumber, FilterType, NotFlag, FieldTypeParameters...)
    not_flag must be present positionally; pass None for blank placeholder.
    """
    return DDERequestView(
        func_name='ViewFilter',
        params=[clause_number, filter_type, not_flag, *filter_type_parameters],
    )


def view_sort(*field_sort_pairs: str) -> DDERequestView:
    """
    Docs: ViewSort(Field1, Sort1, Field2, Sort2, Field3, Sort3, Field4, Sort4)
    Pass as: field1, sort1, field2, sort2, ...
    """
    if (len(field_sort_pairs) % 2) != 0:
        raise ValueError('ViewSort requires even args: Field, Sort pairs.')
    if len(field_sort_pairs) > 8:
        raise ValueError('ViewSort supports up to 4 Field/Sort pairs (8 args).')
    return DDERequestView(func_name='ViewSort', params=list(field_sort_pairs))


def view_view(view_name: str | None = None) -> DDERequestView:
    return DDERequestView(func_name='ViewView', params=[view_name])


def view_item_count() -> DDERequestView:
    return DDERequestView(func_name='ViewItemCount', params=[])


def view_field(index: int, field: str) -> DDERequestView:
    return DDERequestView(func_name='ViewField', params=[index, field])


def view_fields(index: int, fields: Sequence[str], delim: str = DELIM) -> DDERequestView:
    return DDERequestView(func_name='ViewFields', params=[index, len(fields), *fields, delim])


def view_item_name(index: int) -> DDERequestView:
    return DDERequestView(func_name='ViewItemName', params=[index])


def view_item_index(name_field_value: str | None = None) -> DDERequestView:
    return DDERequestView(func_name='ViewItemIndex', params=[name_field_value])


def view_connected_count(index: int, connection_name: str, to_category: str) -> DDERequestView:
    return DDERequestView(func_name='ViewConnectedCount', params=[index, connection_name, to_category])


def view_connected_item(index: int, connection_name: str, to_category: str, conn_index: int) -> DDERequestView:
    return DDERequestView(
        func_name='ViewConnectedItem',
        params=[index, connection_name, to_category, conn_index],
    )


def view_connected_field(
        index: int,
        connection_name: str,
        to_category: str,
        conn_index: int,
        field: str
) -> DDERequestView:
    return DDERequestView(
        func_name='ViewConnectedField',
        params=[index, connection_name, to_category, conn_index, field],
    )


def view_connected_fields(
        index: int,
        connection_name: str,
        to_category: str,
        conn_index: int,
        fields: Sequence[str],
        delim: str | None = None
) -> DDERequestView:
    n = len(fields)
    return DDERequestView(
        func_name='ViewConnectedFields',
        params=[index, connection_name, to_category, conn_index, n, *fields, delim],
    )


def view_mark_item(index: int) -> DDERequestView:
    return DDERequestView(func_name='ViewMarkItem', params=[index])


def view_delete_all_items():
    if input(
            'Are you sure you want to delete ALL items in the current view? This action cannot be undone! (yes/no): '
    ) != 'yes':
        raise RuntimeError('Aborted deletion of all items in view.')
    return 'NOPE'
    # return DDERequest(func_name='ViewDeleteAllItems', params=[])


def view_field_to_file(index: int, field: str, filename: str) -> DDERequestView:
    return DDERequestView(func_name='ViewFieldToFile', params=[index, field, filename])


def view_image_field_to_file(index: int, field: str, filename: str) -> DDERequestView:
    return DDERequestView(func_name='ViewImageFieldToFile', params=[index, field, filename])


def view_save_view(new_view_name: str, shared: str | None = None) -> DDERequestView:
    """
    Docs: shared is "yes" or "no"
    """
    return DDERequestView(func_name='ViewSaveView', params=[new_view_name, shared])
