from pycommence.dde_generators.dde_server import DDEServer
from pycommence.dde_generators.directory import request_msgs
from pycommence.meta.pycmc_fields import CmcDefsDict, CmcFieldDefinition, DELIM
from pycommence.wrapper.conversation_wrapper import DDETopic


class CommenceDDEServer(DDEServer):
    def __init__(self, topic: DDETopic = DDETopic.GET):
        super().__init__(topic)


    def fetch_field_names(self, category: str) -> bool | str | list[str]:
        msg = request_msgs.get_field_names(category)
        field_names = self.send_message(msg)
        return field_names

    def fetch_field_defintion(self, category: str, field_name: str) -> bool | str | list[str]:
        msg = request_msgs.get_field_definition(category, field_name)
        field_definition = self.send_message(msg)
        return field_definition

    def fetch_category_field_definitions_dir(self, category: str) -> CmcDefsDict:
        """ Gets PyCommence connection and retrieves field definitions via DDE for a given category."""
        fields_definitions = CmcDefsDict()
        for field_name in self.fetch_field_names(category):
            field_definition_res = self.fetch_field_defintion(category, field_name)
            field_definition = CmcFieldDefinition.from_field_info(field_definition_res, DELIM)
            fields_definitions[field_name] = field_definition
        return fields_definitions
