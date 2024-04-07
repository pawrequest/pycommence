# """
# API for Commence Cursor objects.
# provides access to the Commence Cursor object and methods to interact with it.
#
# """
# from __future__ import annotations
#
# import typing as _t
# import contextlib
# from functools import cached_property
# from typing import TYPE_CHECKING
#
# from .db_api import Cmc
# from .types_api import CmcError, CmcFilter, Connection, FilterArray
#
# if TYPE_CHECKING:
#     from pycommence.wrapper.cursor import CsrCmc
#
# EmptyKind = _t.Literal['ignore', 'raise']
#
#
# @contextlib.contextmanager
# def csr_context(table_name, cmc_name: str = 'Commence.DB') -> Csr:
#     """Access Commence DB via Csr object context-manager."""
#     try:
#         csr_api = get_csr(table_name, cmc_name)
#         yield csr_api
#     finally:
#         ...
#
#
# def get_csr(table_name, cmc_instance: str = 'Commence.DB') -> Csr:
#     """Create cached connection to Commence and return a Csr to operate on it."""
#     cmc = Cmc(cmc_instance)
#     csr_cmc = cmc.get_cursor(table_name)
#     csr_api = Csr(csr_cmc, db_name=cmc.name)
#     return csr_api
#
#
# class Csr:
#     def __init__(self, cursor: CsrCmc, db_name):
#         self._cursor_cmc = cursor
#         self.db_name = db_name
#
#     @property
#     def category(self):
#         return self._cursor_cmc.category
#
#     @property
#     def column_count(self):
#         return self._cursor_cmc.column_count
#
#     @property
#     def row_count(self):
#         return self._cursor_cmc.row_count
#
#     @property
#     def shared(self):
#         return self._cursor_cmc.shared
#
#     @cached_property
#     def pk_label(self):
#         qs = self._cursor_cmc.get_query_row_set(1)
#         return qs.get_column_label(0)
#
#     def filter_by_field(
#             self,
#             field_name: str,
#             condition: str,
#             value: str = '',
#             *,
#             fslot: int = 1,
#             empty: EmptyKind = 'raise',
#     ) -> None | list[dict[str, str]]:
#         val_cond = f', "{value}"' if value else ''
#         filter_str = f'[ViewFilter({fslot}, F,, {field_name}, {condition}{val_cond})]'  # noqa: E231
#         if not self._cursor_cmc.set_filter(filter_str):
#             if empty == 'raise':
#                 raise CmcError(f'Error setting filter: {filter_str}')
#             if empty == 'ignore':
#                 return
#
#     def filter_by_connection(
#             self,
#             item_name: str,
#             connection: Connection,
#             *,
#             fslot=1
#     ) -> None:
#         filter_str = (f'[ViewFilter({fslot}, CTI,, {connection.name}, '  # noqa: E231
#                       f'{connection.to_table}, {item_name})]')
#         self._cursor_cmc.set_filter(filter_str)
#
#     def filter_by_cmcfil(self, cmc_filter: CmcFilter, slot=1) -> None:
#         self.filter_by_str(cmc_filter.filter_str(slot))
#
#     def filter_by_array(self, fil_array: FilterArray) -> None:
#         for slot, fil in fil_array.filters.items():
#             self.filter_by_cmcfil(fil, slot)
#
#     def filter_by_str(self, filter_str: str):
#         """ commence syntax filter string"""
#         self._cursor_cmc.set_filter(filter_str)
#
#     def clear_filter(self, slot=1):
#         self.filter_by_str(f'[ViewFilter({slot},Clear)]')
#
#     def filter_by_pk(self, pk: str, *, fslot=1, empty: EmptyKind = 'raise'):
#         if not pk:
#             raise ValueError('pk must be a non-empty string')
#         self.filter_by_field(self.pk_label, 'Equal To', value=pk, fslot=fslot, empty=empty)
#         if self.row_count == 0:
#             if empty == 'raise':
#                 raise CmcError(f'No record found for {self.pk_label} {pk}')
#         if self.row_count > 1:
#             raise CmcError(f'Expected 1 record, got {self.row_count}')
#
#     @contextlib.contextmanager
#     def temporary_filter_pk(self, pk: str, *, slot=4, empty: EmptyKind = 'raise'):
#         try:
#             yield self.filter_by_pk(pk, fslot=slot, empty=empty)
#         finally:
#             self.clear_filter(slot)
#
#     @contextlib.contextmanager
#     def temporary_filter_fields(
#             self,
#             field_name: str,
#             condition: str,
#             value: str,
#             *,
#             slot=4,
#             empty: EmptyKind = 'raise'
#     ):
#         try:
#             yield self.filter_by_field(field_name, condition, value, fslot=slot, empty=empty)
#         finally:
#             self.clear_filter(slot)
#
#     def get_named_addset(self, pk_val):
#         row_set = self.get_add_rowset()
#         row_set.modify_row(0, 0, pk_val)
#         return row_set
#
#     def get_add_rowset(self, count=1):
#         return self._cursor_cmc.get_add_row_set(count=count)
#
#     def get_edit_rowset(self, count=1):
#         return self._cursor_cmc.get_edit_row_set(count=count)
#
#     def get_delete_rowset(self, count=1):
#         return self._cursor_cmc.get_delete_row_set(count=count)
#
#     def get_query_rowset(self, count=1):
#         return self._cursor_cmc.get_query_row_set(count=count)
