"""
DDE Execute functions for Commence DDE interface.
- for ViewData and GetData Topics
"""
from __future__ import annotations

from typing import Optional, Union

from ._dde_format import _dde_format_function


def dde_add_item(category: str, item: str, clarify_value: Optional[str] = None) -> str:
    return _dde_format_function("AddItem", [category, item, clarify_value])


def dde_add_shared_item(category: str, item: str) -> str:
    return _dde_format_function("AddSharedItem", [category, item])


def dde_append_text(category: str, item: str, field: str, text: str) -> str:
    return _dde_format_function("AppendText", [category, item, field, text])


def dde_assign_connection(
        from_category: str,
        from_item: str,
        connection_name: str,
        to_category: str,
        to_item: str,
) -> str:
    return _dde_format_function("AssignConnection", [from_category, from_item, connection_name, to_category, to_item])


def dde_unassign_connection(
        from_category: str,
        from_item: str,
        connection_name: str,
        to_category: str,
        to_item: str,
) -> str:
    return _dde_format_function("UnassignConnection", [from_category, from_item, connection_name, to_category, to_item])


def dde_edit_item(category: str, item: str, field: str, value: str) -> str:
    return _dde_format_function("EditItem", [category, item, field, value])


def dde_delete_item(category: str, item: str) -> str:
    return _dde_format_function("DeleteItem", [category, item])


def dde_delete_view(view_name: str) -> str:
    return _dde_format_function("DeleteView", [view_name])


def dde_fire_trigger(trigger: str, *args: str) -> str:
    """
    FireTrigger(Trigger, Arg2..Arg9)
    Accepts up to 8 extra args.
    """
    if len(args) > 8:
        raise ValueError("FireTrigger supports at most 8 extra args (Arg2..Arg9).")
    return _dde_format_function("FireTrigger", [trigger, *args])


def dde_show_desktop(desktop_name: str) -> str:
    return _dde_format_function("ShowDesktop", [desktop_name])


def dde_show_item(category: str, item: str, form_name: Optional[str] = None) -> str:
    return _dde_format_function("ShowItem", [category, item, form_name])


def dde_show_view(view_name: str, force_new_copy: Optional[int] = None) -> str:
    """
    Docs show: [ShowView(View Name, 1)] to force a new copy.
    """
    return _dde_format_function("ShowView", [view_name, force_new_copy])


def dde_get_view_to_file(view_name: str, mode: int, param1: Optional[str], param2: Optional[str], filename: str) -> str:
    return _dde_format_function("GetViewToFile", [view_name, mode, param1, param2, filename])


def dde_check_in_form_script(category: str, form_name: str, filename: str) -> str:
    return _dde_format_function("CheckInFormScript", [category, form_name, filename])


def dde_check_out_form_script(category: str, form_name: str, filename: str) -> str:
    return _dde_format_function("CheckOutFormScript", [category, form_name, filename])


def dde_merge_template_create(name: str, category: str, shared: Union[bool, int]) -> str:
    """
    Docs: MergeTemplateCreate(name, Category, Shared) where Shared is 0|1.
    """
    shared_val = int(shared) if isinstance(shared, bool) else shared
    return _dde_format_function("MergeTemplateCreate", [name, category, shared_val])


def dde_merge_template_save(name: str, shared: Union[bool, int]) -> str:
    shared_val = int(shared) if isinstance(shared, bool) else shared
    return _dde_format_function("MergeTemplateSave", [name, shared_val])


def dde_promote_item_to_shared(category: str, item: str) -> str:
    return _dde_format_function("PromoteItemToShared", [category, item])


def dde_log_phone_call(*category_item_pairs: str) -> str:
    """
    Docs: LogPhoneCall(Category1, Item1, ..., CategoryN, ItemN)
    Pass as: category1, item1, category2, item2, ...
    """
    if len(category_item_pairs) < 2 or (len(category_item_pairs) % 2) != 0:
        raise ValueError("LogPhoneCall requires an even number of args: Category, Item pairs.")
    return _dde_format_function("LogPhoneCall", list(category_item_pairs))
