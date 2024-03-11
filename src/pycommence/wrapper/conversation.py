class CommenceConversation:
    """ Thin Wrapper on Commence's Conversation object using DDE."""
    def __init__(self, cmc_conversation):
        self._conversation = cmc_conversation

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
