"""
DDE Execute functions for Commence DDE interface.
- for ViewData and GetData Topics
"""
from __future__ import annotations


from pycommence.dde_generators.dde_msg import DDEMessage, DDEKind


def execute_add_item(category: str, item: str, clarify_value: str | None = None) -> DDEMessage:
    params = [category, item, clarify_value] # if clarify_value is not None else [category, item]
    return DDEMessage(func_name='AddItem', params=params, kind=DDEKind.EXECUTE)


def execute_add_shared_item(category: str, item: str) -> DDEMessage:
    return DDEMessage(func_name='AddSharedItem', params=[category, item], kind=DDEKind.EXECUTE)


def execute_append_text(category: str, item: str, field: str, text: str) -> DDEMessage:
    return DDEMessage(func_name='AppendText', params=[category, item, field, text], kind=DDEKind.EXECUTE)


def execute_assign_connection(
        from_category: str,
        from_item: str,
        connection_name: str,
        to_category: str,
        to_item: str,
) -> DDEMessage:
    return DDEMessage(func_name='AssignConnection', params=[from_category, from_item, connection_name, to_category, to_item], kind=DDEKind.EXECUTE)


def execute_unassign_connection(
        from_category: str,
        from_item: str,
        connection_name: str,
        to_category: str,
        to_item: str,
) -> DDEMessage:
    return DDEMessage(func_name='UnassignConnection', params=[from_category, from_item, connection_name, to_category, to_item], kind=DDEKind.EXECUTE)


def execute_edit_item(category: str, item: str, field: str, value: str) -> DDEMessage:
    return DDEMessage(func_name='EditItem', params=[category, item, field, value], kind=DDEKind.EXECUTE)


def execute_delete_item(category: str, item: str) -> DDEMessage:
    return DDEMessage(func_name='DeleteItem', params=[category, item], kind=DDEKind.EXECUTE)


def execute_delete_view(view_name: str) -> DDEMessage:
    return DDEMessage(func_name='DeleteView', params=[view_name], kind=DDEKind.EXECUTE)


def execute_fire_trigger(trigger: str, *args: str) -> DDEMessage:
    """
    FireTrigger(Trigger, Arg2..Arg9)
    Accepts up to 8 extra args.
    """
    if len(args) > 8:
        raise ValueError('FireTrigger supports at most 8 extra args (Arg2..Arg9).')
    return DDEMessage(func_name='FireTrigger', params=[trigger, *args], kind=DDEKind.EXECUTE)


def execute_show_desktop(desktop_name: str) -> DDEMessage:
    return DDEMessage(func_name='ShowDesktop', params=[desktop_name], kind=DDEKind.EXECUTE)


def execute_show_item(category: str, item: str, form_name: str | None = None) -> DDEMessage:
    return DDEMessage(func_name='ShowItem', params=[category, item, form_name], kind=DDEKind.EXECUTE)


def execute_show_view(view_name: str, force_new_copy: int | None = None) -> DDEMessage:
    """
    Docs show: [ShowView(View Name, 1)] to force a new copy.
    """
    return DDEMessage(func_name='ShowView', params=[view_name, force_new_copy], kind=DDEKind.EXECUTE)


def execute_get_view_to_file(view_name: str, mode: int, param1: str | None, param2: str | None, filename: str) -> DDEMessage:
    return DDEMessage(func_name='GetViewToFile', params=[view_name, mode, param1, param2, filename], kind=DDEKind.EXECUTE)


def execute_check_in_form_script(category: str, form_name: str, filename: str) -> DDEMessage:
    return DDEMessage(func_name='CheckInFormScript', params=[category, form_name, filename], kind=DDEKind.EXECUTE)


def execute_check_out_form_script(category: str, form_name: str, filename: str) -> DDEMessage:
    return DDEMessage(func_name='CheckOutFormScript', params=[category, form_name, filename], kind=DDEKind.EXECUTE)


def execute_merge_template_create(name: str, category: str, shared: bool | int) -> DDEMessage:
    """
    Docs: MergeTemplateCreate(name, Category, Shared) where Shared is 0|1.
    """
    shared_val = int(shared) if isinstance(shared, bool) else shared
    return DDEMessage(func_name='MergeTemplateCreate', params=[name, category, shared_val], kind=DDEKind.EXECUTE)


def execute_merge_template_save(name: str, shared: bool | int) -> DDEMessage:
    shared_val = int(shared) if isinstance(shared, bool) else shared
    return DDEMessage(func_name='MergeTemplateSave', params=[name, shared_val], kind=DDEKind.EXECUTE)


def execute_promote_item_to_shared(category: str, item: str) -> DDEMessage:
    return DDEMessage(func_name='PromoteItemToShared', params=[category, item], kind=DDEKind.EXECUTE)


def execute_log_phone_call(*category_item_pairs: str) -> DDEMessage:
    """
    Docs: LogPhoneCall(Category1, Item1, ..., CategoryN, ItemN)
    Pass as: category1, item1, category2, item2, ...
    """
    if len(category_item_pairs) < 2 or (len(category_item_pairs) % 2) != 0:
        raise ValueError('LogPhoneCall requires an even number of args: Category, Item pairs.')
    return DDEMessage(func_name='LogPhoneCall', params=list(category_item_pairs), kind=DDEKind.EXECUTE)

# """
# DDE Execute functions for Commence DDE interface.
# - for ViewData and GetData Topics
# """
# from __future__ import annotations
#
# from typing import Optional, Union
#
# from pycommence.dde_generators.dde_msg import DDEMessage
#
#
# def execute_add_item(category: str, item: str, clarify_value: Optional[str] = None) -> DDEMessage:
#     params = [category, item, clarify_value] if clarify_value is not None else [category, item]
#     # params = [category, item, clarify_value]
#     return DDEMessage(func_name="AddItem", params=params)
#
#
# def execute_add_shared_item(category: str, item: str) -> DDEMessage:
#     return DDEMessage(func_name="AddSharedItem", params=[category, item])
#
#
# def execute_append_text(category: str, item: str, field: str, text: str) -> DDEMessage:
#     return DDEMessage(func_name="AppendText", params=[category, item, field, text])
#
#
# def execute_assign_connection(
#         from_category: str,
#         from_item: str,
#         connection_name: str,
#         to_category: str,
#         to_item: str,
# ) -> DDEMessage:
#     return DDEMessage(func_name="AssignConnection", params=[from_category, from_item, connection_name, to_category, to_item])
#
#
# def execute_unassign_connection(
#         from_category: str,
#         from_item: str,
#         connection_name: str,
#         to_category: str,
#         to_item: str,
# ) -> DDEMessage:
#     return DDEMessage(func_name="UnassignConnection", params=[from_category, from_item, connection_name, to_category, to_item])
#
#
# def execute_edit_item(category: str, item: str, field: str, value: str) -> DDEMessage:
#     return DDEMessage(func_name="EditItem", params=[category, item, field, value])
#
#
# def execute_delete_item(category: str, item: str) -> DDEMessage:
#     return DDEMessage(func_name="DeleteItem", params=[category, item])
#
#
# def execute_delete_view(view_name: str) -> DDEMessage:
#     return DDEMessage(func_name="DeleteView", params=[view_name])
#
#
# def execute_fire_trigger(trigger: str, *args: str) -> DDEMessage:
#     """
#     FireTrigger(Trigger, Arg2..Arg9)
#     Accepts up to 8 extra args.
#     """
#     if len(args) > 8:
#         raise ValueError("FireTrigger supports at most 8 extra args (Arg2..Arg9).")
#     return DDEMessage(func_name="FireTrigger", params=[trigger, *args])
#
#
# def execute_show_desktop(desktop_name: str) -> DDEMessage:
#     return DDEMessage(func_name="ShowDesktop", params=[desktop_name])
#
#
# def execute_show_item(category: str, item: str, form_name: Optional[str] = None) -> DDEMessage:
#     return DDEMessage(func_name="ShowItem", params=[category, item, form_name])
#
#
# def execute_show_view(view_name: str, force_new_copy: Optional[int] = None) -> DDEMessage:
#     """
#     Docs show: [ShowView(View Name, 1)] to force a new copy.
#     """
#     return DDEMessage(func_name="ShowView", params=[view_name, force_new_copy])
#
#
# def execute_get_view_to_file(view_name: str, mode: int, param1: Optional[str], param2: Optional[str], filename: str) -> DDEMessage:
#     return DDEMessage(func_name="GetViewToFile", params=[view_name, mode, param1, param2, filename])
#
#
# def execute_check_in_form_script(category: str, form_name: str, filename: str) -> DDEMessage:
#     return DDEMessage(func_name="CheckInFormScript", params=[category, form_name, filename])
#
#
# def execute_check_out_form_script(category: str, form_name: str, filename: str) -> DDEMessage:
#     return DDEMessage(func_name="CheckOutFormScript", params=[category, form_name, filename])
#
#
# def execute_merge_template_create(name: str, category: str, shared: Union[bool, int]) -> DDEMessage:
#     """
#     Docs: MergeTemplateCreate(name, Category, Shared) where Shared is 0|1.
#     """
#     shared_val = int(shared) if isinstance(shared, bool) else shared
#     return DDEMessage(func_name="MergeTemplateCreate", params=[name, category, shared_val])
#
#
# def execute_merge_template_save(name: str, shared: Union[bool, int]) -> DDEMessage:
#     shared_val = int(shared) if isinstance(shared, bool) else shared
#     return DDEMessage(func_name="MergeTemplateSave", params=[name, shared_val])
#
#
# def execute_promote_item_to_shared(category: str, item: str) -> DDEMessage:
#     return DDEMessage(func_name="PromoteItemToShared", params=[category, item])
#
#
# def execute_log_phone_call(*category_item_pairs: str) -> DDEMessage:
#     """
#     Docs: LogPhoneCall(Category1, Item1, ..., CategoryN, ItemN)
#     Pass as: category1, item1, category2, item2, ...
#     """
#     if len(category_item_pairs) < 2 or (len(category_item_pairs) % 2) != 0:
#         raise ValueError("LogPhoneCall requires an even number of args: Category, Item pairs.")
#     return DDEMessage(func_name="LogPhoneCall", params=list(category_item_pairs))