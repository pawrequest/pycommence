from pprint import pprint

from win32com.universal import com_error

from pycommence.api import CmcConnectionCached, add_record, delete_record, filter_by_field, filter_by_name
from pycommence.entities import CmcError

TEST_RECORD_NAME = " _TestRecord"
TEST_PACKAGE_ADD = {'Delivery Contact': 'Fake Deliv contact', 'To Customer': 'Test'}
TEST_PACKAGE_EDIT = {'Delivery Contact': 'Edited del contact', 'To Customer': 'Edited Test'}
LOG_FILE = 'pycommence.log'


def addy_record():
    try:
        db = CmcConnectionCached()
        cursor = db.get_cursor(name='Hire')

        add_result = add_record(cursor, record_name=TEST_RECORD_NAME, package=TEST_PACKAGE_ADD)
        assert add_result, "Record addition failed"
    except com_error as e:
        # todo this is horrible. the error is due to threading but we are not using threading?
        if e.hresult == -2147483617:
            raise CmcError('Record already exists')
    except Exception:
        ...


def old():
    db = CmcConnectionCached()
    curs = db.get_cursor(name='Hire')

    if filter_by_name(curs, TEST_RECORD_NAME):
        delet = delete_record(curs, TEST_RECORD_NAME)
        curs = db.get_cursor(name='Hire')
    add = add_record(curs, record_name=TEST_RECORD_NAME, package=TEST_PACKAGE_ADD)
    ...
    curs = db.get_cursor(name='Hire')
    del_row = delete_record(curs, record_name=TEST_RECORD_NAME)
    ...

    # main()
    # adding()
    # this_year()
    # addy_record()
    # old()


def this_year():
    cmc_db = CmcConnectionCached()
    cursor = cmc_db.get_cursor('Hire')
    filter_by_field(cursor, 'Send Out Date', 'After', 'Last year')
    count = cursor.row_count
    qs = cursor.get_query_row_set(count)
    dicts = qs.get_rows_dict(count)
    sorted_by_send_date = sorted(dicts, key=lambda x: x['Send Out Date'])
    pprint(sorted_by_send_date[:5])
    ...
