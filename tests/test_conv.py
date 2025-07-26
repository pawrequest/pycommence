import pytest

from pycommence.pycommence_v2 import PyCommence
from pycommence.wrapper.cmc_wrapper import CommenceWrapper
from pycommence.wrapper.conversation_wrapper import ConversationTopic


def test_it():
    cmc = CommenceWrapper()
    conversation = cmc.get_conversation_api(ConversationTopic.VIEW_DATA)
    print(conversation.get_field_definition('Contact', 'firstName'))
    ...


@pytest.fixture
def pyc_conv():
    return PyCommence.with_conversation(ConversationTopic.VIEW_DATA)


def test_pyc2(pyc_conv):
    print(pyc_conv.conversations[ConversationTopic.VIEW_DATA].get_field_definition('Contact', 'firstName'))
    ...


def test_view_view(pyc_conv):
    ret = pyc_conv.conversations[ConversationTopic.VIEW_DATA].view_view('Contact List')
    print('\nRESULT OF VIEW_VIEW =', ret.upper())
