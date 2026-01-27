from enum import StrEnum
from typing import Optional, Sequence

from pycommence.dde_generators.dde_msg import DDEMessage
from pycommence.meta.pycmc_fields import DELIM
from pycommence.wrapper.conversation_wrapper import DDETopic


def view_category(category: str) -> DDEMessage:
    return DDEMessage(func_name="ViewCategory", params=[category], topic=DDETopic.VIEW)


def view_conjunction(
        and_or_12: Optional[str] = None,
        and_or_13: Optional[str] = None,
        and_or_34: Optional[str] = None
) -> DDEMessage:
    return DDEMessage(func_name="ViewConjunction", params=[and_or_12, and_or_13, and_or_34], topic=DDETopic.VIEW)


def view_filter(
        clause_number: int,
        filter_type: str,
        not_flag: Optional[str],
        *filter_type_parameters: Optional[str]
) -> DDEMessage:
    """
    Docs: ViewFilter(ClauseNumber, FilterType, NotFlag, FieldTypeParameters...)
    not_flag must be present positionally; pass None for blank placeholder.
    """
    return DDEMessage(
        func_name="ViewFilter",
        params=[clause_number, filter_type, not_flag, *filter_type_parameters],
        topic=DDETopic.VIEW
    )


def view_sort(*field_sort_pairs: str) -> DDEMessage:
    """
    Docs: ViewSort(Field1, Sort1, Field2, Sort2, Field3, Sort3, Field4, Sort4)
    Pass as: field1, sort1, field2, sort2, ...
    """
    if (len(field_sort_pairs) % 2) != 0:
        raise ValueError("ViewSort requires even args: Field, Sort pairs.")
    if len(field_sort_pairs) > 8:
        raise ValueError("ViewSort supports up to 4 Field/Sort pairs (8 args).")
    return DDEMessage(func_name="ViewSort", params=list(field_sort_pairs), topic=DDETopic.VIEW)


def view_view(view_name: Optional[str] = None) -> DDEMessage:
    return DDEMessage(func_name="ViewView", params=[view_name], topic=DDETopic.VIEW)


def view_item_count() -> DDEMessage:
    return DDEMessage(func_name="ViewItemCount", params=[], topic=DDETopic.VIEW)


def view_field(index: int, field: str) -> DDEMessage:
    return DDEMessage(func_name="ViewField", params=[index, field], topic=DDETopic.VIEW)


def view_fields(index: int, fields: Sequence[str], delim: str = DELIM) -> DDEMessage:
    n = len(fields)
    return DDEMessage(func_name="ViewFields", params=[index, n, *fields, delim], topic=DDETopic.VIEW)


def view_item_name(index: int) -> DDEMessage:
    return DDEMessage(func_name="ViewItemName", params=[index], topic=DDETopic.VIEW)


def view_item_index(name_field_value: Optional[str] = None) -> DDEMessage:
    return DDEMessage(func_name="ViewItemIndex", params=[name_field_value], topic=DDETopic.VIEW)


def view_connected_count(index: int, connection_name: str, to_category: str) -> DDEMessage:
    return DDEMessage(func_name="ViewConnectedCount", params=[index, connection_name, to_category], topic=DDETopic.VIEW)


def view_connected_item(index: int, connection_name: str, to_category: str, conn_index: int) -> DDEMessage:
    return DDEMessage(
        func_name="ViewConnectedItem",
        params=[index, connection_name, to_category, conn_index],
        topic=DDETopic.VIEW
    )


def view_connected_field(index: int, connection_name: str, to_category: str, conn_index: int, field: str) -> DDEMessage:
    return DDEMessage(
        func_name="ViewConnectedField",
        params=[index, connection_name, to_category, conn_index, field],
        topic=DDETopic.VIEW
    )


def view_connected_fields(
        index: int,
        connection_name: str,
        to_category: str,
        conn_index: int,
        fields: Sequence[str],
        delim: Optional[str] = None
) -> DDEMessage:
    n = len(fields)
    return DDEMessage(
        func_name="ViewConnectedFields",
        params=[index, connection_name, to_category, conn_index, n, *fields, delim],
        topic=DDETopic.VIEW
    )


def view_mark_item(index: int) -> DDEMessage:
    return DDEMessage(func_name="ViewMarkItem", params=[index], topic=DDETopic.VIEW)


def view_delete_all_items() -> DDEMessage:
    return DDEMessage(func_name="ViewDeleteAllItems", params=[], topic=DDETopic.VIEW)


def view_field_to_file(index: int, field: str, filename: str) -> DDEMessage:
    return DDEMessage(func_name="ViewFieldToFile", params=[index, field, filename], topic=DDETopic.VIEW)


def view_image_field_to_file(index: int, field: str, filename: str) -> DDEMessage:
    return DDEMessage(func_name="ViewImageFieldToFile", params=[index, field, filename], topic=DDETopic.VIEW)


def view_save_view(new_view_name: str, shared: Optional[str] = None) -> DDEMessage:
    """
    Docs: shared is "yes" or "no"
    """
    return DDEMessage(func_name="ViewSaveView", params=[new_view_name, shared], topic=DDETopic.VIEW)


class DDECmdView(StrEnum):
    CATEGORY = "ViewCategory"
    CONJUNCTION = "ViewConjunction"
    FILTER = "ViewFilter"
    SORT = "ViewSort"
    VIEW = "ViewView"
    ITEM_COUNT = "ViewItemCount"
    FIELD = "ViewField"
    FIELDS = "ViewFields"
    ITEM_NAME = "ViewItemName"
    ITEM_INDEX = "ViewItemIndex"
    CONNECTED_COUNT = "ViewConnectedCount"
    CONNECTED_ITEM = "ViewConnectedItem"
    CONNECTED_FIELD = "ViewConnectedField"
    CONNECTED_FIELDS = "ViewConnectedFields"
    MARK_ITEM = "ViewMarkItem"
    DELETE_ALL_ITEMS = "ViewDeleteAllItems"
    FIELD_TO_FILE = "ViewFieldToFile"
    IMAGE_FIELD_TO_FILE = "ViewImageFieldToFile"
    SAVE_VIEW = "ViewSaveView"
