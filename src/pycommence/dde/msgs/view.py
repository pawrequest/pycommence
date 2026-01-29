from collections.abc import Sequence

from pycommence.dde.types import DDERequest, DDETopic
from pycommence.core.fields import DELIM


def view_category(category: str, topic=DDETopic.VIEW) -> DDERequest:
    return DDERequest(func_name='ViewCategory', params=[category], topic=topic)


def view_conjunction(
        and_or_12: str | None = None,
        and_or_13: str | None = None,
        and_or_34: str | None = None
) -> DDERequest:
    return DDERequest(func_name='ViewConjunction', params=[and_or_12, and_or_13, and_or_34], topic=DDETopic.VIEW)


def view_filter(
        clause_number: int,
        filter_type: str,
        not_flag: str | None,
        *filter_type_parameters: str | None
) -> DDERequest:
    """
    Docs: ViewFilter(ClauseNumber, FilterType, NotFlag, FieldTypeParameters...)
    not_flag must be present positionally; pass None for blank placeholder.
    """
    return DDERequest(
        func_name='ViewFilter',
        params=[clause_number, filter_type, not_flag, *filter_type_parameters],
        topic=DDETopic.VIEW
    )


def view_sort(*field_sort_pairs: str) -> DDERequest:
    """
    Docs: ViewSort(Field1, Sort1, Field2, Sort2, Field3, Sort3, Field4, Sort4)
    Pass as: field1, sort1, field2, sort2, ...
    """
    if (len(field_sort_pairs) % 2) != 0:
        raise ValueError('ViewSort requires even args: Field, Sort pairs.')
    if len(field_sort_pairs) > 8:
        raise ValueError('ViewSort supports up to 4 Field/Sort pairs (8 args).')
    return DDERequest(func_name='ViewSort', params=list(field_sort_pairs), topic=DDETopic.VIEW)


def view_view(view_name: str | None = None) -> DDERequest:
    return DDERequest(func_name='ViewView', params=[view_name], topic=DDETopic.VIEW)


def view_item_count() -> DDERequest:
    return DDERequest(func_name='ViewItemCount', params=[], topic=DDETopic.VIEW)


def view_field(index: int, field: str) -> DDERequest:
    return DDERequest(func_name='ViewField', params=[index, field], topic=DDETopic.VIEW)


def view_fields(index: int, fields: Sequence[str], delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='ViewFields', params=[index, len(fields), *fields, delim], topic=DDETopic.VIEW)


def view_item_name(index: int) -> DDERequest:
    return DDERequest(func_name='ViewItemName', params=[index], topic=DDETopic.VIEW)


def view_item_index(name_field_value: str | None = None) -> DDERequest:
    return DDERequest(func_name='ViewItemIndex', params=[name_field_value], topic=DDETopic.VIEW)


def view_connected_count(index: int, connection_name: str, to_category: str) -> DDERequest:
    return DDERequest(func_name='ViewConnectedCount', params=[index, connection_name, to_category], topic=DDETopic.VIEW)


def view_connected_item(index: int, connection_name: str, to_category: str, conn_index: int) -> DDERequest:
    return DDERequest(
        func_name='ViewConnectedItem',
        params=[index, connection_name, to_category, conn_index],
        topic=DDETopic.VIEW
    )


def view_connected_field(index: int, connection_name: str, to_category: str, conn_index: int, field: str) -> DDERequest:
    return DDERequest(
        func_name='ViewConnectedField',
        params=[index, connection_name, to_category, conn_index, field],
        topic=DDETopic.VIEW
    )


def view_connected_fields(
        index: int,
        connection_name: str,
        to_category: str,
        conn_index: int,
        fields: Sequence[str],
        delim: str | None = None
) -> DDERequest:
    n = len(fields)
    return DDERequest(
        func_name='ViewConnectedFields',
        params=[index, connection_name, to_category, conn_index, n, *fields, delim],
        topic=DDETopic.VIEW
    )


def view_mark_item(index: int) -> DDERequest:
    return DDERequest(func_name='ViewMarkItem', params=[index], topic=DDETopic.VIEW)


def view_delete_all_items():
    if input(
            'Are you sure you want to delete ALL items in the current view? This action cannot be undone! (yes/no): '
    ) != 'yes':
        raise RuntimeError('Aborted deletion of all items in view.')
    return
    # return DDERequest(func_name='ViewDeleteAllItems', params=[], topic=DDETopic.VIEW)


def view_field_to_file(index: int, field: str, filename: str) -> DDERequest:
    return DDERequest(func_name='ViewFieldToFile', params=[index, field, filename], topic=DDETopic.VIEW)


def view_image_field_to_file(index: int, field: str, filename: str) -> DDERequest:
    return DDERequest(func_name='ViewImageFieldToFile', params=[index, field, filename], topic=DDETopic.VIEW)


def view_save_view(new_view_name: str, shared: str | None = None) -> DDERequest:
    """
    Docs: shared is "yes" or "no"
    """
    return DDERequest(func_name='ViewSaveView', params=[new_view_name, shared], topic=DDETopic.VIEW)
