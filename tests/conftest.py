# @pytest.fixture(autouse=True)
# def delay_between_tests():
#     yield
#     time.sleep(1)


# @pytest.fixture(scope='function', autouse=True)
# def com_setup():
#     pythoncom.CoInitialize()
#     yield
#     pythoncom.CoUninitialize()


JEFF_DICT = {
    'contactKey': 'Bezos.Jeff',
    'homeAddress': '',
    'businessNumber': '1800 3000 9009',
    'homeNumber': '',
    'faxNumber': '',
    'Notes': '',
    'Nickname': '',
    'Extension': '',
    'Title': 'CEO of Amazon',
    'mobileNumber': '',
    'pagerNumber': '',
    'Birthday': '',
    'emailHome': '',
    'firstName': 'Jeff',
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
    'Relates to Account': 'Amazon',
    'Relates to Opportunity': '',
    'LinkedInLink': '',
    'Relates to mailingType': '',
    'Relates to Attachment': '',
    'twitterLink': 'https://twitter.com/jeffbezos',
    'Relates to Address': 'Customer service PO Box',
    'Relates to History': '',
    'Relates to Expense': '',
    'FacebookLink': 'https://www.facebook.com/groups/1654560838132448/',
    'Relates to contactType': '',
    'Relates to contactInterest': '',
    'Relates to Employee': 'Simpson.Barry.T',
    'Handheld Device Employee': 'Simpson.Barry.T',
    'ID': '27BH1B',
    'cityStateZip': 'Seattle, WA 98109',
    'Influence': 'Low',
    'Relates to detailNote': '',
    'Manager of Contact': '',
    'Managed by Contact': '',
    'isPrimary': 'FALSE',
    'Relates to Salutation': 'Mr.',
}
GEOFF_DICT = {
    'Account': 'Amazon',
    'Birthday': '',
    'City': '',
    'DOB': '',
    'Extension': '',
    'FacebookLink': 'https://www.facebook.com/groups/1654560838132448/',
    'Handheld Device Employee': 'Simpson.Barry.T',
    'ID': '27BH1B',
    'Influence': 'Low',
    'LinkedInLink': '',
    'MI': '',
    'Managed by Contact': '',
    'Manager of Contact': '',
    'Nickname': '',
    'Notes': 'GEOFF',
    'Relates to Account': 'Amazon',
    'Relates to Activity': '',
    'Relates to Address': 'Customer service PO Box',
    'Relates to Attachment': '',
    'Relates to Employee': 'Simpson.Barry.T',
    'Relates to Expense': '',
    'Relates to History': '',
    'Relates to Opportunity': '',
    'Relates to Salutation': 'Mr.',
    'Relates to contactInterest': '',
    'Relates to contactType': '',
    'Relates to detailNote': '',
    'Relates to mailingType': '',
    'Salutation': 'None',
    'Title': 'CEO of Amazon',
    'addModifyDate': '20190815',
    'addModifyUser': 'Simpson.Barry.T',
    'busCity': 'Seattle',
    'busCountry': 'USA',
    'busState': 'WA',
    'busStreet': '410 Terry Ave N',
    'busZip': '98109',
    'businessNumber': '1800 3000 9009',
    'cityStateZip': 'Seattle, WA 98109',
    'contactKey': 'Bezos.Geoff',
    'doNotSolicit': 'FALSE',
    'emailBusiness': '',
    'emailHome': '',
    'faxNumber': '',
    'firstName': 'Geoff',
    'homeAddress': 'GEOFF',
    'homeNumber': '',
    'isPrimary': 'FALSE',
    'lastContact': '20190807',
    'lastName': 'Bezos',
    'mailCode': '',
    'mainTelephone': '',
    'mobileNumber': '',
    'nextContact': '',
    'otherTelephone': '',
    'pagerNumber': '',
    'properName': 'Mr. Jeff Bezos',
    'spouseName': '',
    'stateProvince': '',
    'twitterLink': 'https://twitter.com/jeffbezos',
    'zipPostal': '',
}
RICHARD_KEY = 'Branson.Richard'
GEOFF_KEY = GEOFF_DICT.get('contactKey')
JEFF_KEY = JEFF_DICT.get('contactKey')

UPDATE_PKG_1 = {'firstName': 'test2', 'doNotSolicit': 'TRUE'}
PK_VAL = 'Col0 Val'
__all__ = ['JEFF_DICT', 'GEOFF_DICT', 'GEOFF_KEY', 'JEFF_KEY', 'UPDATE_PKG_1']
