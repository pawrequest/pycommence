from __future__ import annotations

from pycommence.wrapper.cmc_types import CmcFieldDefinition


class CommenceConversation:
    """ Thin Wrapper on Commence's Conversation object using DDE."""

    def __init__(self, cmc_conversation):
        self._conversation = cmc_conversation
        self.delim = r";*;%"

    def execute(self, dde_command: str) -> bool:
        """
        Executes the DDE Command.

        Args:
            dde_command (str): The DDE command to execute.

        Returns:
            bool: True on successful execution, False otherwise.
        """
        return self._conversation.Execute(dde_command)

    def request(self, dde_command: str) -> str:
        """
        Processes the DDE Request.

        Args:
            dde_command (str): The DDE command to process.

        Returns:
            str: The result of processing the DDE request.
        """
        return self._conversation.Request(dde_command)

    def get_field_definition(self, category_name: str, field_name: str) -> CmcFieldDefinition:
        """
        Get the Field Definition for a given field in a category.

        Args:
            category_name (str): The Category name.
            field_name (str): The Field name.

        Returns:
            CmcFieldDefinition: The Field Definition.
        """
        dde_command = f"[GetFieldDefinition({category_name}, {field_name}, {self.delim})]"

        finfo = self.request(dde_command)
        return CmcFieldDefinition.from_field_info(finfo)


