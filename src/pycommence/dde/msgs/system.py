from enum import StrEnum

from pycommence.dde.types import DDESystemRequest, DDETopic


def databases() -> DDESystemRequest:
    """Generate DDE request for Databases."""
    return DDESystemRequest(func_name='Databases', params=[], topic=DDETopic.SYSTEM)


def formats() -> DDESystemRequest:
    """Generate DDE request for Formats."""
    return DDESystemRequest(func_name='Formats', params=[], topic=DDETopic.SYSTEM)


def status(status: bool | None = None) -> DDESystemRequest:
    """Generate DDE request for Status."""
    if status is not None:
        return DDESystemRequest(func_name='Status', params=[True if status else False], topic=DDETopic.SYSTEM)
    return DDESystemRequest(func_name='Status', topic=DDETopic.SYSTEM)


def sysitems() -> DDESystemRequest:
    """Generate DDE request for SysItems."""
    return DDESystemRequest(func_name='SysItems', params=[], topic=DDETopic.SYSTEM)


def topics() -> DDESystemRequest:
    """Generate DDE request for Topics."""
    return DDESystemRequest(func_name='Topics', params=[], topic=DDETopic.SYSTEM)


def version() -> DDESystemRequest:
    """Generate DDE request for Version."""
    return DDESystemRequest(func_name='Version', params=[], topic=DDETopic.SYSTEM)


def version_extended() -> DDESystemRequest:
    """Generate DDE request for VersionExtended."""
    return DDESystemRequest(func_name='VersionExtended', params=[], topic=DDETopic.SYSTEM)

class SystemMessageEnum(StrEnum):
    DATABASES = 'Databases'
    FORMATS = 'Formats'
    STATUS = 'Status'
    SYSITEMS = 'SysItems'
    TOPICS = 'Topics'
    VERSION = 'Version'
    VERSION_EXTENDED = 'VersionExtended'