from enum import StrEnum

from pycommence.dde_generators.dde_msg import DDEMessage, DDEKind
from pycommence.wrapper.conversation_wrapper import DDETopic


def system_databases() -> DDEMessage:
    """Generate DDE request for Databases."""
    return DDEMessage(func_name="Databases", params=[], topic=DDETopic.SYSTEM)


def system_formats() -> DDEMessage:
    """Generate DDE request for Formats."""
    return DDEMessage(func_name="Formats", params=[], topic=DDETopic.SYSTEM)


def system_status() -> DDEMessage:
    """Generate DDE request for Status."""
    return DDEMessage(func_name="Status", params=[], topic=DDETopic.SYSTEM)


def system_sysitems() -> DDEMessage:
    """Generate DDE request for SysItems."""
    return DDEMessage(func_name="SysItems", params=[], topic=DDETopic.SYSTEM)


def system_topics() -> DDEMessage:
    """Generate DDE request for Topics."""
    return DDEMessage(func_name="Topics", params=[], topic=DDETopic.SYSTEM)


def system_version() -> DDEMessage:
    """Generate DDE request for Version."""
    return DDEMessage(func_name="Version", params=[], topic=DDETopic.SYSTEM)


def system_version_extended() -> DDEMessage:
    """Generate DDE request for VersionExtended."""
    return DDEMessage(func_name="VersionExtended", params=[], topic=DDETopic.SYSTEM)

