# @pytest.fixture(autouse=True)
# def delay_between_tests():
#     yield
#     time.sleep(1)
import pytest

from pycommence.pycmc_types import CursorType
from pycommence.pycommence_v2 import PyCommence

JEFF_DICT = {
    'contactKey': 'Bezos.Jeff',
    'businessNumber': '1800 3000 9009',
    'Title': 'CEO of Amazon',
    'firstName': 'Jeff',
    'properName': 'Mr. Jeff Bezos',
    'lastName': 'Bezos',
    'busCity': 'Seattle',
    'busCountry': 'USA',
    'busState': 'WA',
    'busStreet': '410 Terry Ave N',
    'busZip': '98109',
    'Account': 'Amazon',
    'addModifyUser': 'Simpson.Barry.T',
    'addModifyDate': '20190815',
    'lastContact': '20190807',
    'twitterLink': 'https://twitter.com/jeffbezos',
    'FacebookLink': 'https://www.facebook.com/groups/1654560838132448/',
    'ID': '27BH1B',
    'cityStateZip': 'Seattle, WA 98109',
    'Influence': 'Low',
    'isPrimary': 'FALSE',
}

JEFF_EDITED_DICT = {
    'contactKey': 'Bezos.Geoff',
    'homeAddress': 'GEOFF',
    'businessNumber': '1800 3000 9009',
    'homeNumber': '',
    'faxNumber': '',
    'Notes': 'GEOFF',
    'Nickname': '',
    'Extension': '',
    'Title': 'CEO of Amazon',
    'mobileNumber': '',
    'pagerNumber': '',
    'Birthday': '',
    'emailHome': '',
    'firstName': 'Geoff',
    'MI': '',
    'Salutation': 'None',
    'City': '',
    'stateProvince': '',
    'zipPostal': '',
    'properName': 'Mr. Jeff Bezos',
    'spouseName': '',
    'lastName': 'Bezos',
    'emailBusiness': '',
    'doNotSolicit': 'FALSE',
    'busCity': 'Seattle',
    'busCountry': 'USA',
    'busState': 'WA',
    'busStreet': '410 Terry Ave N',
    'busZip': '98109',
    'Account': 'Amazon',
    'otherTelephone': '',
    'mainTelephone': '',
    'addModifyUser': 'Simpson.Barry.T',
    'addModifyDate': '20190815',
    'mailCode': '',
    'nextContact': '',
    'lastContact': '20190807',
    'DOB': '',
    'Relates to Activity': '',
    'Relates to Account': '',
    'Relates to Opportunity': '',
    'LinkedInLink': '',
    'Relates to mailingType': '',
    'Relates to Attachment': '',
    'twitterLink': 'https://twitter.com/jeffbezos',
    'Relates to Address': '',
    'Relates to History': '',
    'Relates to Expense': '',
    'FacebookLink': '',
    'Relates to contactType': '',
    'Relates to contactInterest': '',
    'Relates to Employee': '',
    'Handheld Device Employee': '',
    'ID': '',
    'cityStateZip': 'Seattle, WA 98109',
    'Influence': 'Low',
    'Relates to detailNote': '',
    'Manager of Contact': '',
    'Managed by Contact': '',
    'isPrimary': 'FALSE',
    'Relates to Salutation': '',
}

NEW_DICT = {
    'contactKey': 'Guy.Some',
    'businessNumber': '1800 3000 9009',
    'Title': 'CEO of SOMmeBix',
    'Notes': 'Some Notes',
    'Nickname': 'somnivkbname',
    'lastName': 'Guy',
    'firstName': 'Some',
}

NEW_DICT_RESPONSE = {
    'Account': '',
    'Birthday': '',
    'City': '',
    'DOB': '',
    'Extension': '',
    'FacebookLink': '',
    'Handheld Device Employee': '',
    'ID': '',
    'Influence': 'Low',
    'LinkedInLink': '',
    'MI': '',
    'Managed by Contact': '',
    'Manager of Contact': '',
    'Nickname': 'somnivkbname',
    'Notes': 'Some Notes',
    'Relates to Account': '',
    'Relates to Activity': '',
    'Relates to Address': '',
    'Relates to Attachment': '',
    'Relates to Employee': '',
    'Relates to Expense': '',
    'Relates to History': '',
    'Relates to Opportunity': '',
    'Relates to Salutation': '',
    'Relates to contactInterest': '',
    'Relates to contactType': '',
    'Relates to detailNote': '',
    'Relates to mailingType': '',
    'Salutation': 'None',
    'Title': 'CEO of SOMmeBix',
    'addModifyDate': '',
    'addModifyUser': '',
    'busCity': '',
    'busCountry': '',
    'busState': '',
    'busStreet': '',
    'busZip': '',
    'businessNumber': '1800 3000 9009',
    'cityStateZip': '',
    'contactKey': 'Some.Guy',
    'doNotSolicit': 'FALSE',
    'emailBusiness': '',
    'emailHome': '',
    'faxNumber': '',
    'firstName': '',
    'homeAddress': '',
    'homeNumber': '',
    'isPrimary': 'FALSE',
    'lastContact': '20240629',
    'lastName': '',
    'mailCode': '',
    'mainTelephone': '',
    'mobileNumber': '',
    'nextContact': '',
    'otherTelephone': '',
    'pagerNumber': '',
    'properName': '',
    'spouseName': '',
    'stateProvince': '',
    'twitterLink': '',
    'zipPostal': '',
}

UPDATE_DICT = {
    'businessNumber': '1800 3000 3333',
    'Title': 'CEO of AnotherBix',
    'Notes': 'Updated Notes',
}

JEFF_KEY = JEFF_DICT.get('contactKey')
FNAME = NEW_DICT.get('firstName')
LNAME = NEW_DICT.get('lastName')
NEW_KEY = NEW_DICT.get('contactKey')


def get_new_pycmc(tblname: str | None = None):
    pycmc = PyCommence()
    if tblname:
        pycmc.set_csr(csrname=tblname)
    if not pycmc.cmc_wrapper.name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    return pycmc


def pycmc_view_cursor():
    pycmc = PyCommence.with_csr('All Contacts-By Company', mode=CursorType.VIEW)
    if not pycmc.cmc_wrapper.delivery_contact_name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    return pycmc


def pyc_contact_new():
    return get_new_pycmc('Contact')


@pytest.fixture(scope='function', params=[pyc_contact_new])
# @pytest.fixture(scope='function', params=[pyc_contact_new, pycmc_view_cursor])
def pycmc(request) -> PyCommence:
    param = request.param
    return param()


__all__ = [
    'JEFF_DICT',
    'JEFF_EDITED_DICT',
    'JEFF_KEY',
    'NEW_DICT',
    'UPDATE_DICT',
    'NEW_KEY',
]
