from collections.abc import Sequence

from pycommence.dde.types import DDERequestGet
from pycommence.pycommence_options import get_options

DELIM = get_options().delim


# -------------------------
# REQUEST items (GetData / ViewData)
# -------------------------

def clarify_item_names(status: bool | None = None) -> DDERequestGet:
    """
    Docs: [ClarifyItemNames(Status)]
    If left blank, status is queried.
    """
    if status is None:
        return DDERequestGet(func_name='ClarifyItemNames', params=[])
    return DDERequestGet(func_name='ClarifyItemNames', params=[True if status else False])


def active_view_info(delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetActiveViewInfo', params=[delim])


def caller_id(category: str | None, phone_number: str, delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetCallerID', params=[category, phone_number, delim])


def category_count() -> DDERequestGet:
    return DDERequestGet(func_name='GetCategoryCount')


def category_definition(category: str, delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetCategoryDefinition', params=[category, delim])


def category_names(delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetCategoryNames', params=[delim])


def connection_count(category: str) -> DDERequestGet:
    return DDERequestGet(func_name='GetConnectionCount', params=[category])


def connection_names(category: str, delim: str = DELIM, conn_cat_delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetConnectionNames', params=[category, delim, conn_cat_delim])


def database(delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetDatabase', params=[delim])


def database_definition(delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetDatabaseDefinition', params=[delim])


def desktop_count() -> DDERequestGet:
    return DDERequestGet(func_name='GetDesktopCount')


def desktop_names(delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetDesktopNames', params=[delim])


def field(category: str, item: str, field: str) -> DDERequestGet:
    return DDERequestGet(func_name='GetField', params=[category, item, field])


def fields(category: str, item: str, fields: Sequence[str], delim: str = DELIM) -> DDERequestGet:
    n = len(fields)
    params = [category, item, n] + list(fields) + [delim]
    return DDERequestGet(func_name='GetFields', params=params)


def field_count(category: str) -> DDERequestGet:
    return DDERequestGet(func_name='GetFieldCount', params=[category])


def field_definition(category: str, field: str, delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetFieldDefinition', params=[category, field, delim])


def field_names(category: str, delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetFieldNames', params=[category, delim])


def field_to_file(category: str, item: str, field: str, filename: str) -> DDERequestGet:
    return DDERequestGet(func_name='GetFieldToFile', params=[category, item, field, filename])


def form_count(category: str) -> DDERequestGet:
    return DDERequestGet(func_name='GetFormCount', params=[category])


def form_names(category: str, delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetFormNames', params=[category, delim])


def image_field_count(category: str) -> DDERequestGet:
    return DDERequestGet(func_name='GetImageFieldCount', params=[category])


def image_field_names(category: str, delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetImageFieldNames', params=[category, delim])


def image_field_to_file(category: str, item: str, field: str, filename: str) -> DDERequestGet:
    return DDERequestGet(func_name='GetImageFieldToFile', params=[category, item, field, filename])


def item_count(category: str) -> DDERequestGet:
    return DDERequestGet(func_name='GetItemCount', params=[category], returns=[int])


def item_names(category: str, delim: str | None = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetItemNames', params=[category, delim])


def last_error() -> DDERequestGet:
    return DDERequestGet(func_name='GetLastError')


def mark_item(category: str, item: str, clarify_value: str | None = None) -> DDERequestGet:
    """
    Docs: GetMarkItem(Category, Item, Clarify Value)
    Also supports: GetMarkItem("(-Me-)")
    """
    params = [category, item, clarify_value] if clarify_value is not None else [category, item]
    return DDERequestGet(func_name='GetMarkItem', params=params)


def mark_active_item() -> DDERequestGet:
    return DDERequestGet(func_name='MarkActiveItem')


def phone_number(phone_number: str) -> DDERequestGet:
    return DDERequestGet(func_name='GetPhoneNumber', params=[phone_number])


def preference(setting: str, delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetPreference', params=[setting, delim])


def reverse_name(name: str, pref_flag: int | None = None) -> DDERequestGet:
    return DDERequestGet(func_name='GetReverseName', params=[name, pref_flag])


def trigger_count() -> DDERequestGet:
    return DDERequestGet(func_name='GetTriggerCount')


def trigger_names(delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetTriggerNames', params=[delim])


def view_count(category: str | None = None) -> DDERequestGet:
    return DDERequestGet(func_name='GetViewCount', params=[category])


def view_names(category: str | None = None, delim: str = DELIM) -> DDERequestGet:
    return DDERequestGet(func_name='GetViewNames', params=[category, delim])
