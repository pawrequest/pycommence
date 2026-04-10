"""Tests for pycommence.dde.msgs.system"""

from pycommence.dde.msgs import system
from pycommence.dde.types import DDETopic


class TestSystemMessages:
    def test_databases(self):
        msg = system.databases()
        assert msg.func_name == 'Databases'
        assert msg.topic == DDETopic.SYSTEM

    def test_formats(self):
        msg = system.formats()
        assert msg.func_name == 'Formats'

    def test_status_query(self):
        msg = system.status()
        assert str(msg) == 'Status'

    def test_status_set_true(self):
        msg = system.status(True)
        assert 'yes' in str(msg)

    def test_version(self):
        msg = system.version()
        assert msg.func_name == 'Version'

    def test_version_extended(self):
        msg = system.version_extended()
        assert msg.func_name == 'VersionExtended'

    def test_sysitems(self):
        msg = system.sysitems()
        assert msg.func_name == 'SysItems'

    def test_topics(self):
        msg = system.topics()
        assert msg.func_name == 'Topics'
