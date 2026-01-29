from enum import StrEnum

from pycommence.dde.types import DDESystemMessage, DDETopic


def system_databases() -> DDESystemMessage:
    """Generate DDE request for Databases."""
    return DDESystemMessage(func_name='Databases', params=[], topic=DDETopic.SYSTEM)


def system_formats() -> DDESystemMessage:
    """Generate DDE request for Formats."""
    return DDESystemMessage(func_name='Formats', params=[], topic=DDETopic.SYSTEM)


def system_status(status: bool | None = None) -> DDESystemMessage:
    """Generate DDE request for Status."""
    if status is not None:
        return DDESystemMessage(func_name='Status', params=[True if status else False], topic=DDETopic.SYSTEM)
    return DDESystemMessage(func_name='Status', topic=DDETopic.SYSTEM)


def system_sysitems() -> DDESystemMessage:
    """Generate DDE request for SysItems."""
    return DDESystemMessage(func_name='SysItems', params=[], topic=DDETopic.SYSTEM)


def system_topics() -> DDESystemMessage:
    """Generate DDE request for Topics."""
    return DDESystemMessage(func_name='Topics', params=[], topic=DDETopic.SYSTEM)


def system_version() -> DDESystemMessage:
    """Generate DDE request for Version."""
    return DDESystemMessage(func_name='Version', params=[], topic=DDETopic.SYSTEM)


def system_version_extended() -> DDESystemMessage:
    """Generate DDE request for VersionExtended."""
    return DDESystemMessage(func_name='VersionExtended', params=[], topic=DDETopic.SYSTEM)

class SystemMessageEnum(StrEnum):
    DATABASES = 'Databases'
    FORMATS = 'Formats'
    STATUS = 'Status'
    SYSITEMS = 'SysItems'
    TOPICS = 'Topics'
    VERSION = 'Version'
    VERSION_EXTENDED = 'VersionExtended'