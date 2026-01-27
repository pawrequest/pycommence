"""
Request Data
GetDara an
"""
from collections.abc import Sequence

from pycommence.client_dde.dde_msg import _dde_format_function
from pycommence.fields import DELIM


# -------------------------
# REQUEST items (GetData / ViewData)
# -------------------------

def dde_clarify_item_names(status: bool | None = None) -> str:
    """
    Docs: [ClarifyItemNames(Status)]
    If left blank, status is queried.
    """
    if status is None:
        return _dde_format_function('ClarifyItemNames')
        # return _dde_bracket_call("ClarifyItemNames", [None])
    return _dde_format_function('ClarifyItemNames', ['True' if status else 'False'])


def dde_get_active_view_info(delim: str = DELIM) -> str:
    return _dde_format_function('GetActiveViewInfo', [delim])


def dde_get_caller_id(category: str | None, phone_number: str, delim: str = DELIM) -> str:
    return _dde_format_function('GetCallerID', [category, phone_number, delim])


def dde_get_category_count() -> str:
    return _dde_format_function('GetCategoryCount', [])


def dde_get_category_definition(category: str, delim: str = DELIM) -> str:
    return _dde_format_function('GetCategoryDefinition', [category, delim])


def dde_get_category_names(delim: str = DELIM) -> str:
    return _dde_format_function('GetCategoryNames', [delim])


def dde_get_connection_count(category: str) -> str:
    return _dde_format_function('GetConnectionCount', [category])


def dde_get_connection_names(category: str, delim: str = DELIM, conn_cat_delim: str = DELIM) -> str:
    return _dde_format_function('GetConnectionNames', [category, delim, conn_cat_delim])


def dde_get_database(delim: str = DELIM) -> str:
    return _dde_format_function('GetDatabase', [delim])


def dde_get_database_definition(delim: str = DELIM) -> str:
    return _dde_format_function('GetDatabaseDefinition', [delim])


def dde_get_desktop_count() -> str:
    return _dde_format_function('GetDesktopCount', [])


def dde_get_desktop_names(delim: str = DELIM) -> str:
    return _dde_format_function('GetDesktopNames', [delim])


def dde_get_field(category: str, item: str, field: str) -> str:
    return _dde_format_function('GetField', [category, item, field])


def dde_get_fields(category: str, item: str, fields: Sequence[str], delim: str = DELIM) -> str:
    """
    Docs: GetFields(Category, Item, n, Field_1..., Field_n, Delim)
    """
    n = len(fields)
    return _dde_format_function('GetFields', [category, item, n, *fields, delim])


def dde_get_field_count(category: str) -> str:
    return _dde_format_function('GetFieldCount', [category])


def dde_get_field_definition(category: str, field: str, delim: str = DELIM) -> str:
    return _dde_format_function('GetFieldDefinition', [category, field, delim])


def dde_get_field_names(category: str, delim: str = DELIM) -> str:
    return _dde_format_function('GetFieldNames', [category, delim])


def dde_get_field_to_file(category: str, item: str, field: str, filename: str) -> str:
    return _dde_format_function('GetFieldToFile', [category, item, field, filename])


def dde_get_form_count(category: str) -> str:
    return _dde_format_function('GetFormCount', [category])


def dde_get_form_names(category: str, delim: str = DELIM) -> str:
    return _dde_format_function('GetFormNames', [category, delim])


def dde_get_image_field_count(category: str) -> str:
    return _dde_format_function('GetImageFieldCount', [category])


def dde_get_image_field_names(category: str, delim: str = DELIM) -> str:
    return _dde_format_function('GetImageFieldNames', [category, delim])


def dde_get_image_field_to_file(category: str, item: str, field: str, filename: str) -> str:
    return _dde_format_function('GetImageFieldToFile', [category, item, field, filename])


def dde_get_item_count(category: str) -> str:
    return _dde_format_function('GetItemCount', [category])


def dde_get_item_names(category: str, delim: str | None = DELIM) -> str:
    return _dde_format_function('GetItemNames', [category, delim])


def dde_get_last_error() -> str:
    return _dde_format_function('GetLastError')


def dde_get_mark_item(category: str, item: str | None = None, clarify_value: str | None = None) -> str:
    """
    Docs: GetMarkItem(Category, Item, Clarify Value)
    Also supports: GetMarkItem("(-Me-)")
    """
    return _dde_format_function('GetMarkItem', [category, item, clarify_value])


def dde_mark_active_item() -> str:
    return _dde_format_function('MarkActiveItem', [])


def dde_get_phone_number(phone_number: str) -> str:
    return _dde_format_function('GetPhoneNumber', [phone_number])


def dde_get_preference(setting: str, delim: str = DELIM) -> str:
    return _dde_format_function('GetPreference', [setting, delim])


def dde_get_reverse_name(name: str, pref_flag: int | None = None) -> str:
    return _dde_format_function('GetReverseName', [name, pref_flag])


def dde_get_trigger_count() -> str:
    return _dde_format_function('GetTriggerCount', [])


def dde_get_trigger_names(delim: str = DELIM) -> str:
    return _dde_format_function('GetTriggerNames', [delim])


def dde_get_view_count(category: str | None = None) -> str:
    return _dde_format_function('GetViewCount', [category])


def dde_get_view_names(category: str | None = None, delim: str = DELIM) -> str:
    return _dde_format_function('GetViewNames', [category, delim])
