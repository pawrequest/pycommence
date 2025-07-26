import pytest

from pycommence.pycommence_v2 import PyCommence
from pycommence.wrapper.cmc_wrapper import CommenceWrapper


def test_it():
    cmc = CommenceWrapper()
    conversation = cmc.get_conversation_api('ViewData')
    print(conversation.get_field_definition('Contact', 'firstName'))
    ...


@pytest.fixture
def pyc_conv():
    return PyCommence.with_conversation('ViewData')


def test_pyc2(pyc_conv):
    print(pyc_conv.conversation.get_field_definition('Contact', 'firstName'))
    ...


def test_view_view(pyc_conv):
    ret = pyc_conv.conversation.view_view('newView')
