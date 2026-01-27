from typing import Optional, Sequence

from pycommence.dde_generators.dde_msg import DDEMessage
from pycommence.meta.pycmc_fields import DELIM


# -------------------------
# REQUEST items (GetData / ViewData)
# -------------------------

def clarify_item_names(status: Optional[bool] = None) -> DDEMessage:
    """
    Docs: [ClarifyItemNames(Status)]
    If left blank, status is queried.
    """
    if status is None:
        return DDEMessage(func_name="ClarifyItemNames", params=[])
    return DDEMessage(func_name="ClarifyItemNames", params=[True if status else False])


def get_active_view_info(delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetActiveViewInfo", params=[delim])


def get_caller_id(category: Optional[str], phone_number: str, delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetCallerID", params=[category, phone_number, delim])


def get_category_count() -> DDEMessage:
    return DDEMessage(func_name="GetCategoryCount", params=[])


def get_category_definition(category: str, delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetCategoryDefinition", params=[category, delim])


def get_category_names(delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetCategoryNames", params=[delim])


def get_connection_count(category: str) -> DDEMessage:
    return DDEMessage(func_name="GetConnectionCount", params=[category])


def get_connection_names(category: str, delim: str = DELIM, conn_cat_delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetConnectionNames", params=[category, delim, conn_cat_delim])


def get_database(delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetDatabase", params=[delim])


def get_database_definition(delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetDatabaseDefinition", params=[delim])


def get_desktop_count() -> DDEMessage:
    return DDEMessage(func_name="GetDesktopCount", params=[])


def get_desktop_names(delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetDesktopNames", params=[delim])


def get_field(category: str, item: str, field: str) -> DDEMessage:
    return DDEMessage(func_name="GetField", params=[category, item, field])


def get_fields(category: str, item: str, fields: Sequence[str], delim: str = DELIM) -> DDEMessage:
    """
    Docs: GetFields(Category, Item, n, Field_1..., Field_n, Delim)
    """
    n = len(fields)
    params = [category, item, n] + list(fields) + [delim]
    return DDEMessage(func_name="GetFields", params=params)


def get_field_count(category: str) -> DDEMessage:
    return DDEMessage(func_name="GetFieldCount", params=[category])


def get_field_definition(category: str, field: str, delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetFieldDefinition", params=[category, field, delim])


def get_field_names(category: str, delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetFieldNames", params=[category, delim])


def get_field_to_file(category: str, item: str, field: str, filename: str) -> DDEMessage:
    return DDEMessage(func_name="GetFieldToFile", params=[category, item, field, filename])


def get_form_count(category: str) -> DDEMessage:
    return DDEMessage(func_name="GetFormCount", params=[category])


def get_form_names(category: str, delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetFormNames", params=[category, delim])


def get_image_field_count(category: str) -> DDEMessage:
    return DDEMessage(func_name="GetImageFieldCount", params=[category])


def get_image_field_names(category: str, delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetImageFieldNames", params=[category, delim])


def get_image_field_to_file(category: str, item: str, field: str, filename: str) -> DDEMessage:
    return DDEMessage(func_name="GetImageFieldToFile", params=[category, item, field, filename])


def get_item_count(category: str) -> DDEMessage:
    return DDEMessage(func_name="GetItemCount", params=[category])


def get_item_names(category: str, delim: Optional[str] = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetItemNames", params=[category, delim])


def get_last_error() -> DDEMessage:
    return DDEMessage(func_name="GetLastError", params=[])


def get_mark_item(category: str, item: str, clarify_value: Optional[str] = None) -> DDEMessage:
    """
    Docs: GetMarkItem(Category, Item, Clarify Value)
    Also supports: GetMarkItem("(-Me-)")
    """
    params = [category, item, clarify_value] if clarify_value is not None else [category, item]
    return DDEMessage(func_name="GetMarkItem", params=params)


def mark_active_item() -> DDEMessage:
    return DDEMessage(func_name="MarkActiveItem", params=[])


def get_phone_number(phone_number: str) -> DDEMessage:
    return DDEMessage(func_name="GetPhoneNumber", params=[phone_number])


def get_preference(setting: str, delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetPreference", params=[setting, delim])


def get_reverse_name(name: str, pref_flag: Optional[int] = None) -> DDEMessage:
    return DDEMessage(func_name="GetReverseName", params=[name, pref_flag])


def get_trigger_count() -> DDEMessage:
    return DDEMessage(func_name="GetTriggerCount", params=[])


def get_trigger_names(delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetTriggerNames", params=[delim])


def get_view_count(category: Optional[str] = None) -> DDEMessage:
    return DDEMessage(func_name="GetViewCount", params=[category])


def get_view_names(category: Optional[str] = None, delim: str = DELIM) -> DDEMessage:
    return DDEMessage(func_name="GetViewNames", params=[category, delim])
