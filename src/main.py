from commence_py import CmcDB


def main():
    cmc_db = CmcDB()
    cursor = cmc_db.get_cursor('Hire')
    cursor.filter_by_name('Test - 10/11/2023 ref 42744')
    qs = cursor.get_query_row_set(1)
    dicty = qs.get_rows_dict(1)
    assert dicty[0]['Name'] == 'Test - 10/11/2023 ref 42744'
    ...


def this_year():
    cmc_db = CmcDB()
    cursor = cmc_db.get_cursor('Hire')
    cursor.filter_by_field('Send Out Date', 'After', 'Last year')
    count = cursor.row_count
    qs = cursor.get_query_row_set(count)
    dicts = qs.get_rows_dict(count)
    sorted_by_send_date = sorted(dicts, key=lambda x: x['Send Out Date'])
    ...


def adding():
    cmc_db = CmcDB()
    cursor = cmc_db.get_cursor('Address')
    qs = cursor.get_add_row_set(1)
    qs.modify_row(0, 0, "An address2")
    qs.modify_row(0, 1, "HERES A STRING OF TEXT")
    qs.commit()
    ...


if __name__ == '__main__':
    # main()
    # adding()
    this_year()
