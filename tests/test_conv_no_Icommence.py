# import pytest
#
# from pycommence.contexts import pycommence_conversation_context
# from pycommence.dde_generators.dde_request import dde_get_field_names
# from pycommence.dde_generators.routines import get_item_routine2
# from pycommence.meta.pycmc_fields import DELIM
#
# @pytest.fixture(scope='function')
# def view_conv():
#     with pycommence_conversation_context('ViewData') as conv:
#         yield conv
#
# def test_context(view_conv):
#     response = view_conv.Request(dde_get_field_names('Contact')).split(DELIM)
#     assert 'contactKey' in response
#
# def test_routine(view_conv):
#     res2 = get_item_routine2('Contact', 'Musk.Elon', view_conv)
#     ...
