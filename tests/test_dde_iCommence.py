import pytest

from pycommence import pycommence_context
from pycommence.dde_generators.pycmc_dde.routines import fetch_category_field_definitions, get_item_routine
from pycommence.dde_generators.pycmc_dde.dde_request import (
    dde_get_field_count,
    dde_get_field_names,
    dde_get_item_count,
    dde_get_item_names,
)
from pycommence.wrapper.conversation_wrapper import DDEKind


def test_dde_field_count():
    dde_cmd = dde_get_field_count('Contact')
    cached = '[GetFieldCount("Contact")]'
    assert dde_cmd == cached
    with pycommence_context() as p:  # noqa
        res = p.send_dde(cmd=dde_cmd, topic='Tutorial', kind=DDEKind.REQUEST)
    assert res == '45'


def test_dde_item_count():
    dde_cmd = dde_get_item_count('Contact')
    cached = '[GetItemCount("Contact")]'
    assert dde_cmd == cached
    with pycommence_context() as p:  # noqa
        res = p.send_dde(cmd=dde_cmd, topic='Tutorial', kind=DDEKind.REQUEST)
    assert res == '25'


def test_dde_field_names():
    dde_cmd = dde_get_field_names('Contact')
    with pycommence_context() as p:  # noqa
        res = p.send_dde(cmd=dde_cmd, topic='Tutorial', kind=DDEKind.REQUEST)
    expected = ['contactKey', 'Account', 'addModifyDate', 'addModifyUser', 'Birthday', 'busCity', 'busCountry',
                'businessNumber', 'busState', 'busStreet', 'busZip', 'City', 'cityStateZip', 'DOB', 'doNotSolicit',
                'emailBusiness', 'emailHome', 'Extension', 'FacebookLink', 'faxNumber', 'firstName', 'homeAddress',
                'homeNumber', 'ID', 'Influence', 'isPrimary', 'lastContact', 'lastName', 'LinkedInLink', 'mailCode',
                'mainTelephone', 'MI', 'mobileNumber', 'nextContact', 'Nickname', 'Notes', 'otherTelephone',
                'pagerNumber', 'properName', 'Salutation', 'spouseName', 'stateProvince', 'Title', 'twitterLink',
                'zipPostal']
    assert res == expected


def test_dde_item_names():
    dde_cmd = dde_get_item_names('Contact')
    with pycommence_context() as p:  # noqa
        res = p.send_dde(cmd=dde_cmd, topic='Tutorial', kind=DDEKind.REQUEST)
    expected = ['Bezos.Jeff', 'Branson.Richard', 'Buffett.Warren', 'Carney.Steve', 'Carr.Brian', 'Douglas.Michael',
                'Findlay.Howard', 'Gates.Bill', 'Jennings.Kevin', 'Logan.Andrew', 'Madison.Bruce', 'Malick.Charles',
                'Mark.Kane', 'Melrose.Harry', 'Musk.Elon', 'Nadella.Satya', 'Pichai.Sundar', 'Rubbel.John',
                'Ryder.Philip', 'Spring.Debbie', 'Steele.Patrick', 'Walsh.Peter', 'White.Peter', 'Winfrey.Oprah',
                'Zuckerberg.Mark']
    assert res == expected


@pytest.mark.skip(reason="System Topic Broken?")
def test_system_conv():
    print('FAILS why??')
    with pycommence_context() as p:  # noqa
        cached = '[Status]'
        # ddemsg = dde_formats()
        res = p.send_dde(cmd=cached, topic='System', kind=DDEKind.REQUEST)
    ...


def test_field_definiitions():
    fields_defs = fetch_category_field_definitions('Contact')
    assert len(fields_defs) == 45


def test_get_item():
    res = get_item_routine('Contact', 'Musk.Elon')
    ...
    # expected = ['Vertical Stab Company', 'Simpson.Barry.T', 'Cleveland', 'USA', 'OH', '5578 West 67th Street', '44144',
    #             '', 'Cleveland, OH 44144', '', 'Elon', '', '77OG6P', 'Musk', '', '', '', '', 'Mr. Elon Musk', '', '',
    #             'CEO of SpaceX', '']
    # assert res == expected
