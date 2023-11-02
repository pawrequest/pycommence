from cmc_gpt.cmc_db import CmcDB


def main():
    cmc_db = CmcDB()
    cursor = cmc_db.get_cursor('Hire')
    cursor.seek_row(1, 3000)
    qs = cursor.get_query_row_set(20)
    dicty = qs.get_rows_dict(20)
    ...


if __name__ == '__main__':
    main()
