from collections.abc import Sequence

from pycommence.dde.types import DDERequest
from pycommence.core.fields import DELIM


# -------------------------
# REQUEST items (GetData / ViewData)
# -------------------------

def clarify_item_names(status: bool | None = None) -> DDERequest:
    """
    Docs: [ClarifyItemNames(Status)]
    If left blank, status is queried.
    """
    if status is None:
        return DDERequest(func_name='ClarifyItemNames', params=[])
    return DDERequest(func_name='ClarifyItemNames', params=[True if status else False])


def get_active_view_info(delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetActiveViewInfo', params=[delim])


def get_caller_id(category: str | None, phone_number: str, delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetCallerID', params=[category, phone_number, delim])


def get_category_count() -> DDERequest:
    return DDERequest(func_name='GetCategoryCount')


def get_category_definition(category: str, delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetCategoryDefinition', params=[category, delim])


def get_category_names(delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetCategoryNames', params=[delim])


def get_connection_count(category: str) -> DDERequest:
    return DDERequest(func_name='GetConnectionCount', params=[category])


def get_connection_names(category: str, delim: str = DELIM, conn_cat_delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetConnectionNames', params=[category, delim, conn_cat_delim])


def get_database(delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetDatabase', params=[delim])


def get_database_definition(delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetDatabaseDefinition', params=[delim])


def get_desktop_count() -> DDERequest:
    return DDERequest(func_name='GetDesktopCount')


def get_desktop_names(delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetDesktopNames', params=[delim])


def get_field(category: str, item: str, field: str) -> DDERequest:
    return DDERequest(func_name='GetField', params=[category, item, field])


def get_fields(category: str, item: str, fields: Sequence[str], delim: str = DELIM) -> DDERequest:
    """
    Docs: GetFields(Category, Item, n, Field_1..., Field_n, Delim)
    """
    n = len(fields)
    params = [category, item, n] + list(fields) + [delim]
    return DDERequest(func_name='GetFields', params=params)


def get_field_count(category: str) -> DDERequest:
    return DDERequest(func_name='GetFieldCount', params=[category])


def get_field_definition(category: str, field: str, delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetFieldDefinition', params=[category, field, delim])


def get_field_names(category: str, delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetFieldNames', params=[category, delim])


def get_field_to_file(category: str, item: str, field: str, filename: str) -> DDERequest:
    return DDERequest(func_name='GetFieldToFile', params=[category, item, field, filename])


def get_form_count(category: str) -> DDERequest:
    return DDERequest(func_name='GetFormCount', params=[category])


def get_form_names(category: str, delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetFormNames', params=[category, delim])


def get_image_field_count(category: str) -> DDERequest:
    return DDERequest(func_name='GetImageFieldCount', params=[category])


def get_image_field_names(category: str, delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetImageFieldNames', params=[category, delim])


def get_image_field_to_file(category: str, item: str, field: str, filename: str) -> DDERequest:
    return DDERequest(func_name='GetImageFieldToFile', params=[category, item, field, filename])


def get_item_count(category: str) -> DDERequest:
    return DDERequest(func_name='GetItemCount', params=[category], returns=[int])


def get_item_names(category: str, delim: str | None = DELIM) -> DDERequest:
    return DDERequest(func_name='GetItemNames', params=[category, delim])


def get_last_error() -> DDERequest:
    return DDERequest(func_name='GetLastError')


def get_mark_item(category: str, item: str, clarify_value: str | None = None) -> DDERequest:
    """
    Docs: GetMarkItem(Category, Item, Clarify Value)
    Also supports: GetMarkItem("(-Me-)")
    """
    params = [category, item, clarify_value] if clarify_value is not None else [category, item]
    return DDERequest(func_name='GetMarkItem', params=params)


def mark_active_item() -> DDERequest:
    return DDERequest(func_name='MarkActiveItem')


def get_phone_number(phone_number: str) -> DDERequest:
    return DDERequest(func_name='GetPhoneNumber', params=[phone_number])


def get_preference(setting: str, delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetPreference', params=[setting, delim])


def get_reverse_name(name: str, pref_flag: int | None = None) -> DDERequest:
    return DDERequest(func_name='GetReverseName', params=[name, pref_flag])


def get_trigger_count() -> DDERequest:
    return DDERequest(func_name='GetTriggerCount')


def get_trigger_names(delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetTriggerNames', params=[delim])


def get_view_count(category: str | None = None) -> DDERequest:
    return DDERequest(func_name='GetViewCount', params=[category])


def get_view_names(category: str | None = None, delim: str = DELIM) -> DDERequest:
    return DDERequest(func_name='GetViewNames', params=[category, delim])
