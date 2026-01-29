from pycommence import pycommence_context
from pycommence.com.dde_routines import fetch_category_field_definitions, get_item_routine
from pycommence.core.fields import DELIM
from pycommence.dde import msgs
from sample_data import CONTACT_FIELD_NAMES, CONTACT_ITEM_NAMES


def test_dde_field_count():
    msg = msgs.request.get_field_count('Contact')
    cached = '[GetFieldCount("Contact")]'
    assert str(msg) == cached
    with pycommence_context() as p:
        res = p.send_dde_msg(msg)
    assert res == '45'


def test_dde_item_count():
    msg = msgs.request.get_item_count('Contact')
    cached = '[GetItemCount("Contact")]'
    assert str(msg) == cached
    with pycommence_context() as p:
        res = p.send_dde_msg(msg)
    assert res == '25'


def test_dde_field_names():
    msg = msgs.request.get_field_names('Contact')
    cached = f'[GetFieldNames("Contact","{DELIM}")]'
    assert str(msg) == cached
    with pycommence_context() as p:
        res = p.send_dde_msg(msg)
    assert res == CONTACT_FIELD_NAMES


def test_dde_item_names():
    msg = msgs.request.get_item_names('Contact')
    with pycommence_context() as p:
        res = p.send_dde_msg(msg)
    assert res == CONTACT_ITEM_NAMES


def test_system_conv():
    msg = msgs.system.system_status()
    with pycommence_context() as p:
        assert p.send_dde_msg(msg) == 'Ready', 'System is not ready'


def test_field_definiitions():
    fields_defs = fetch_category_field_definitions('Contact')
    assert len(fields_defs) == 45


def test_get_item():
    res = get_item_routine('Contact', 'Musk.Elon')
    assert res
    ...
    # expected = ['Vertical Stab Company', 'Simpson.Barry.T', 'Cleveland', 'USA', 'OH', '5578 West 67th Street', '44144',
    #             '', 'Cleveland, OH 44144', '', 'Elon', '', '77OG6P', 'Musk', '', '', '', '', 'Mr. Elon Musk', '', '',
    #             'CEO of SpaceX', '']
    # assert res == expected
