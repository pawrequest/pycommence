# @pytest.fixture(autouse=True)
# def delay_between_tests():
#     yield
#     time.sleep(1)
import pytest

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
    'contactKey': 'Bezos.Geoff', 'homeAddress': 'GEOFF', 'businessNumber': '1800 3000 9009', 'homeNumber': '',
    'faxNumber': '', 'Notes': 'GEOFF', 'Nickname': '', 'Extension': '', 'Title': 'CEO of Amazon', 'mobileNumber': '',
    'pagerNumber': '', 'Birthday': '', 'emailHome': '', 'firstName': 'Geoff', 'MI': '', 'Salutation': 'None',
    'City': '', 'stateProvince': '', 'zipPostal': '', 'properName': 'Mr. Jeff Bezos', 'spouseName': '',
    'lastName': 'Bezos', 'emailBusiness': '', 'doNotSolicit': 'FALSE', 'busCity': 'Seattle', 'busCountry': 'USA',
    'busState': 'WA', 'busStreet': '410 Terry Ave N', 'busZip': '98109', 'Account': 'Amazon', 'otherTelephone': '',
    'mainTelephone': '', 'addModifyUser': 'Simpson.Barry.T', 'addModifyDate': '20190815', 'mailCode': '',
    'nextContact': '', 'lastContact': '20190807', 'DOB': '', 'Relates to Activity': '', 'Relates to Account': '',
    'Relates to Opportunity': '', 'LinkedInLink': '', 'Relates to mailingType': '', 'Relates to Attachment': '',
    'twitterLink': 'https://twitter.com/jeffbezos', 'Relates to Address': '', 'Relates to History': '',
    'Relates to Expense': '', 'FacebookLink': '', 'Relates to contactType': '', 'Relates to contactInterest': '',
    'Relates to Employee': '', 'Handheld Device Employee': '', 'ID': '', 'cityStateZip': 'Seattle, WA 98109',
    'Influence': 'Low', 'Relates to detailNote': '', 'Manager of Contact': '', 'Managed by Contact': '',
    'isPrimary': 'FALSE', 'Relates to Salutation': ''
}
NEW_DICT = {
    'contactKey': 'Some.Guy',
    'businessNumber': '1800 3000 9009',
    'Title': 'CEO of Amazon',
    'firstName': 'Some',
    'properName': 'Mr. Some Guy',
    'lastName': 'Guy',
    'busCity': 'Seattle',
    'busCountry': 'USA',
    'busState': 'WA',
    'busStreet': '410 Terry Ave N',
}

RICHARD_KEY = 'Branson.Richard'
JEFF_EDITED_KEY = JEFF_EDITED_DICT.get('contactKey')
JEFF_KEY = JEFF_DICT.get('contactKey')

UPDATE_PKG_1 = {'firstName': 'test2', 'doNotSolicit': 'TRUE'}
PK_VAL = 'Col0 Val'


def pyc_contact_old():
    from pycommence import PyCommence
    from pycommence.cursor import get_csr
    csr = get_csr('Contact')
    if not csr.db_name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    return PyCommence(csr=csr)


def get_new_pycmc(tblname: str | None = None):
    from pycommence.pyc2 import PyCommence
    pycmc = PyCommence()
    if tblname:
        pycmc.set_csr(tblname=tblname)
    if not pycmc.cmc_wrapper.name == 'Tutorial':
        raise ValueError('Expected Tutorial DB')
    return pycmc


def pyc_contact_new():
    return get_new_pycmc('Contact')


def pyc_empty_new():
    return get_new_pycmc()


@pytest.fixture(scope='session', params=[pyc_contact_old, pyc_contact_new])
def pyc_contact_prm(request):
    param = request.param
    return param()


@pytest.fixture(scope='session')
def new_dict():
    return NEW_DICT


@pytest.fixture(scope='session')
def new_key():
    return NEW_DICT.get('contactKey')


@pytest.fixture(scope='session')
def jeff_dict():
    return JEFF_DICT


@pytest.fixture(scope='session')
def jeff_edited_dict():
    return JEFF_EDITED_DICT


@pytest.fixture(scope='session')
def jeff_key():
    return JEFF_KEY


@pytest.fixture(scope='session')
def jeff_edited_key():
    return JEFF_EDITED_KEY


@pytest.fixture(scope='session')
def richard_key():
    return RICHARD_KEY


@pytest.fixture(scope='session')
def update_pkg_1():
    return UPDATE_PKG_1


@pytest.fixture(scope='session')
def pk_val():
    return PK_VAL


__all__ = ['JEFF_DICT', 'JEFF_EDITED_DICT', 'JEFF_EDITED_KEY', 'JEFF_KEY', 'UPDATE_PKG_1', 'PK_VAL', 'RICHARD_KEY']
