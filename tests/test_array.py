from amherst.commence import INITIAL_HIRE_FILTER
from pycommence import PyCommence


def test_records():
    with PyCommence.from_table_name_context(table_name='Hire') as py_cmc:
        fil = INITIAL_HIRE_FILTER
        print('Filter:', fil)
        records = py_cmc.records_by_array(fil)
        print(len(records), 'records found.')
        [
            print(record['Name'], 'Status:', record['Status'], 'Send Date:', record['Send Out Date'])
            for record in records
        ]
        assert records
