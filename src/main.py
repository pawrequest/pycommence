from .commence_py import CmcDB


def main():
    cmc_db = CmcDB()
    cursor = cmc_db.get_cursor('Hire')
    cursor.seek_row(1, 3000)
    qs = cursor.get_query_row_set(20)
    dicty = qs.get_rows_dict(20)
    ...


def adding():
    cmc_db = CmcDB()
    cursor = cmc_db.get_cursor('Address')
    qs = cursor.get_add_row_set(1)
    qs.mo


if __name__ == '__main__':
    main()
