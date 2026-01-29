"""
DDE Execute functions for Commence DDE interface.
- for ViewData and GetData Topics
"""
from __future__ import annotations

from pycommence.dde.types import DDEExecuteBase, DDETopic


def add_item(
        category: str,
        item: str,
        topic: DDETopic,
        clarify_value: str | None = None,
) -> DDEExecuteBase:
    params = [category, item, clarify_value]  # if clarify_value is not None else [category, item]
    msg = DDEExecuteBase(func_name='AddItem', params=params)
    msg.topic = topic
    return msg


def add_shared_item(category: str, item: str, topic: DDETopic, ) -> DDEExecuteBase:
    return DDEExecuteBase(func_name='AddSharedItem', params=[category, item], topic=topic)


def append_text(category: str, item: str, field: str, text: str, topic: DDETopic) -> DDEExecuteBase:
    return DDEExecuteBase(func_name='AppendText', params=[category, item, field, text], topic=topic)


def assign_connection(
        from_category: str,
        from_item: str,
        connection_name: str,
        to_category: str,
        to_item: str,
        topic: DDETopic
) -> DDEExecuteBase:
    return DDEExecuteBase(
        func_name='AssignConnection',
        params=[from_category, from_item, connection_name, to_category, to_item],
        topic=topic
    )


def unassign_connection(
        from_category: str,
        from_item: str,
        connection_name: str,
        to_category: str,
        to_item: str,
        topic: DDETopic
) -> DDEExecuteBase:
    return DDEExecuteBase(
        func_name='UnassignConnection',
        params=[from_category, from_item, connection_name, to_category, to_item],
        topic=topic
    )


def edit_item(category: str, item: str, field: str, value: str, topic: DDETopic) -> DDEExecuteBase:
    return DDEExecuteBase(func_name='EditItem', params=[category, item, field, value], topic=topic)


def delete_item(category: str, item: str, topic: DDETopic) -> DDEExecuteBase:
    return DDEExecuteBase(func_name='DeleteItem', params=[category, item], topic=topic)


def delete_view(view_name: str, topic: DDETopic) -> DDEExecuteBase:
    return DDEExecuteBase(func_name='DeleteView', params=[view_name], topic=topic)


def fire_trigger(trigger: str, *args: str, topic: DDETopic) -> DDEExecuteBase:
    """
    FireTrigger(Trigger, Arg2..Arg9)
    Accepts up to 8 extra args.
    """
    if len(args) > 8:
        raise ValueError('FireTrigger supports at most 8 extra args (Arg2..Arg9).')
    return DDEExecuteBase(func_name='FireTrigger', params=[trigger, *args], topic=topic)


def show_desktop(desktop_name: str, topic: DDETopic) -> DDEExecuteBase:
    return DDEExecuteBase(func_name='ShowDesktop', params=[desktop_name], topic=topic)


def show_item(category: str, item: str, topic: DDETopic, form_name: str | None = None) -> DDEExecuteBase:
    return DDEExecuteBase(func_name='ShowItem', params=[category, item, form_name], topic=topic)


def show_view(view_name: str, topic: DDETopic, force_new_copy: int | None = None) -> DDEExecuteBase:
    """
    Docs show: [ShowView(View Name, 1)] to force a new copy.
    """
    return DDEExecuteBase(func_name='ShowView', params=[view_name, force_new_copy], topic=topic)


def get_view_to_file(
        view_name: str,
        mode: int,
        param1: str | None,
        param2: str | None,
        filename: str,
        topic: DDETopic,
) -> DDEExecuteBase:
    return DDEExecuteBase(func_name='GetViewToFile', params=[view_name, mode, param1, param2, filename], topic=topic)


def check_in_form_script(category: str, form_name: str, filename: str) -> DDEExecuteBase:
    return DDEExecuteBase(func_name='CheckInFormScript', params=[category, form_name, filename])


def check_out_form_script(category: str, form_name: str, filename: str) -> DDEExecuteBase:
    return DDEExecuteBase(func_name='CheckOutFormScript', params=[category, form_name, filename])


def merge_template_create(name: str, category: str, shared: bool | int) -> DDEExecuteBase:
    """
    Docs: MergeTemplateCreate(name, Category, Shared) where Shared is 0|1.
    """
    shared_val = int(shared) if isinstance(shared, bool) else shared
    return DDEExecuteBase(func_name='MergeTemplateCreate', params=[name, category, shared_val])


def merge_template_save(name: str, shared: bool | int) -> DDEExecuteBase:
    shared_val = int(shared) if isinstance(shared, bool) else shared
    return DDEExecuteBase(func_name='MergeTemplateSave', params=[name, shared_val])


def promote_item_to_shared(category: str, item: str) -> DDEExecuteBase:
    return DDEExecuteBase(func_name='PromoteItemToShared', params=[category, item])


def log_phone_call(*category_item_pairs: str) -> DDEExecuteBase:
    """
    Docs: LogPhoneCall(Category1, Item1, ..., CategoryN, ItemN)
    Pass as: category1, item1, category2, item2, ...
    """
    if len(category_item_pairs) < 2 or (len(category_item_pairs) % 2) != 0:
        raise ValueError('LogPhoneCall requires an even number of args: Category, Item pairs.')
    return DDEExecuteBase(func_name='LogPhoneCall', params=list(category_item_pairs))

# """
# DDE Execute functions for Commence DDE interface.
# - for ViewData and GetData Topics
# """
# from __future__ import annotations
#
# from typing import Optional, Union
#
# from pycommence.pycommence_dde.pycommence_dde import DDEExecute
#
#
# def add_item(category: str, item: str, clarify_value: Optional[str] = None) -> DDEExecute:
#     params = [category, item, clarify_value] if clarify_value is not None else [category, item]
#     # params = [category, item, clarify_value]
#     return DDEExecute(func_name="AddItem", params=params)
#
#
# def add_shared_item(category: str, item: str) -> DDEExecute:
#     return DDEExecute(func_name="AddSharedItem", params=[category, item])
#
#
# def append_text(category: str, item: str, field: str, text: str) -> DDEExecute:
#     return DDEExecute(func_name="AppendText", params=[category, item, field, text])
#
#
# def assign_connection(
#         from_category: str,
#         from_item: str,
#         connection_name: str,
#         to_category: str,
#         to_item: str,
# ) -> DDEExecute:
#     return DDEExecute(func_name="AssignConnection", params=[from_category, from_item, connection_name, to_category, to_item])
#
#
# def unassign_connection(
#         from_category: str,
#         from_item: str,
#         connection_name: str,
#         to_category: str,
#         to_item: str,
# ) -> DDEExecute:
#     return DDEExecute(func_name="UnassignConnection", params=[from_category, from_item, connection_name, to_category, to_item])
#
#
# def edit_item(category: str, item: str, field: str, value: str) -> DDEExecute:
#     return DDEExecute(func_name="EditItem", params=[category, item, field, value])
#
#
# def delete_item(category: str, item: str) -> DDEExecute:
#     return DDEExecute(func_name="DeleteItem", params=[category, item])
#
#
# def delete_view(view_name: str) -> DDEExecute:
#     return DDEExecute(func_name="DeleteView", params=[view_name])
#
#
# def fire_trigger(trigger: str, *args: str) -> DDEExecute:
#     """
#     FireTrigger(Trigger, Arg2..Arg9)
#     Accepts up to 8 extra args.
#     """
#     if len(args) > 8:
#         raise ValueError("FireTrigger supports at most 8 extra args (Arg2..Arg9).")
#     return DDEExecute(func_name="FireTrigger", params=[trigger, *args])
#
#
# def show_desktop(desktop_name: str) -> DDEExecute:
#     return DDEExecute(func_name="ShowDesktop", params=[desktop_name])
#
#
# def show_item(category: str, item: str, form_name: Optional[str] = None) -> DDEExecute:
#     return DDEExecute(func_name="ShowItem", params=[category, item, form_name])
#
#
# def show_view(view_name: str, force_new_copy: Optional[int] = None) -> DDEExecute:
#     """
#     Docs show: [ShowView(View Name, 1)] to force a new copy.
#     """
#     return DDEExecute(func_name="ShowView", params=[view_name, force_new_copy])
#
#
# def get_view_to_file(view_name: str, mode: int, param1: Optional[str], param2: Optional[str], filename: str) -> DDEExecute:
#     return DDEExecute(func_name="GetViewToFile", params=[view_name, mode, param1, param2, filename])
#
#
# def check_in_form_script(category: str, form_name: str, filename: str) -> DDEExecute:
#     return DDEExecute(func_name="CheckInFormScript", params=[category, form_name, filename])
#
#
# def check_out_form_script(category: str, form_name: str, filename: str) -> DDEExecute:
#     return DDEExecute(func_name="CheckOutFormScript", params=[category, form_name, filename])
#
#
# def merge_template_create(name: str, category: str, shared: Union[bool, int]) -> DDEExecute:
#     """
#     Docs: MergeTemplateCreate(name, Category, Shared) where Shared is 0|1.
#     """
#     shared_val = int(shared) if isinstance(shared, bool) else shared
#     return DDEExecute(func_name="MergeTemplateCreate", params=[name, category, shared_val])
#
#
# def merge_template_save(name: str, shared: Union[bool, int]) -> DDEExecute:
#     shared_val = int(shared) if isinstance(shared, bool) else shared
#     return DDEExecute(func_name="MergeTemplateSave", params=[name, shared_val])
#
#
# def promote_item_to_shared(category: str, item: str) -> DDEExecute:
#     return DDEExecute(func_name="PromoteItemToShared", params=[category, item])
#
#
# def log_phone_call(*category_item_pairs: str) -> DDEExecute:
#     """
#     Docs: LogPhoneCall(Category1, Item1, ..., CategoryN, ItemN)
#     Pass as: category1, item1, category2, item2, ...
#     """
#     if len(category_item_pairs) < 2 or (len(category_item_pairs) % 2) != 0:
#         raise ValueError("LogPhoneCall requires an even number of args: Category, Item pairs.")
#     return DDEExecute(func_name="LogPhoneCall", params=list(category_item_pairs))
