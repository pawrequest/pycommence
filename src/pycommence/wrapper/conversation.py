from __future__ import annotations

from pycommence.wrapper._icommence import ICommenceConversation
from pycommence.wrapper.cmc_types import CmcFieldDefinition


class ConversationAPI:
    """ Thin Wrapper on Commence's Conversation object using DDE."""

    def __init__(self, cmc_conversation: ICommenceConversation):
        self._conv_wrapper = cmc_conversation

    def execute(self, dde_command: str) -> bool:
        """
        Executes the DDE Command.

        Args:
            dde_command (str): The DDE command to execute.

        Returns:
            bool: True on successful execution, False otherwise.
        """
        return self._conv_wrapper.Execute(dde_command)

    def request(self, dde_command: str) -> str:
        """
        Processes the DDE Request.

        Args:
            dde_command (str): The DDE command to process.

        Returns:
            str: The result of processing the DDE request.
        """
        return self._conv_wrapper.Request(dde_command)

    def get_field_definition(self, category_name: str, field_name: str, delim: str = r';*;%') -> CmcFieldDefinition:
        """
        Get the Field Definition for a given field in a category.

        Args:
            category_name (str): The Category name.
            field_name (str): The Field name.
            delim (str): The delimiter to use.

        Returns:
            CmcFieldDefinition: The Field Definition.
        """
        dde_command = f'[GetFieldDefinition({category_name}, {field_name}, {delim})]'

        finfo = self.request(dde_command)
        return CmcFieldDefinition.from_field_info(finfo)

    def view_view(self, viewname: str):
        dde_command = rf'[ViewView({viewname})]'
        return self.request(dde_command)
