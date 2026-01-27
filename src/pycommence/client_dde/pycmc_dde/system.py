from enum import StrEnum

from pycommence.client_dde.dde_msg import _dde_format_function


## NOT WORKING??

def dde_databases() -> str:
    """Generate DDE request for Databases."""
    return _dde_format_function('Databases')


def dde_formats() -> str:
    """Generate DDE request for Formats."""
    return _dde_format_function('Formats')


def dde_status() -> str:
    """Generate DDE request for Status."""
    return _dde_format_function('Status')


def dde_sysitems() -> str:
    """Generate DDE request for SysItems."""
    return _dde_format_function('SysItems')


def dde_topics() -> str:
    """Generate DDE request for Topics."""
    return _dde_format_function('Topics')


def dde_version() -> str:
    """Generate DDE request for Version."""
    return _dde_format_function('Version')


def dde_version_extended() -> str:
    """Generate DDE request for VersionExtended."""
    return _dde_format_function('VersionExtended')


class DDECmdSystem(StrEnum):
    DATABASES = 'Databases'
    FORMATS = 'Formats'
    STATUS = 'Status'
    SYSITEMS = 'SysItems'
    TOPICS = 'Topics'
    VERSION = 'Version'
    VERSION_EXTENDED = 'VersionExtended'
