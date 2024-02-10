

# Constants
TEST_RECORD_NAME = "_TestRecord"
TEST_PACKAGE_ADD = {'Delivery Contact': 'Fake Del contact', 'To Customer': 'Test'}
TEST_PACKAGE_EDIT = {'Delivery Contact': 'Edited del contact', 'To Customer': 'Edited Test'}

# @pytest.fixture
# def cmcdb():
#     yield CmcDB()
#
#
# @pytest.fixture
# def new_cursor(cmcdb):
#     def new_curs():
#         return cmcdb.get_cursor('Hire')
#
#     return new_curs


testies = """
def test_add_record():
    db = CmcDB()
    cursor = db.get_cursor('Hire')
    # Add a new record
    add_result = add_record(cursor, TEST_RECORD_NAME, TEST_PACKAGE_ADD)
    assert add_result, "Record addition failed"

    # # Retrieve and verify the added record with a new cursor
    # cursor = new_cursor()
    # added_record = get_record(cursor, TEST_RECORD_NAME)
    # assert added_record, "Failed to retrieve the added record"
    # assert added_record == TEST_PACKAGE_ADD, "Record data does not match added data"


def test_edit_record(cursor):
    # Edit the existing record
    edit_result = edit_record(cursor, TEST_RECORD_NAME, TEST_PACKAGE_EDIT)
    assert edit_result, "Record editing failed"

    # Retrieve and verify the edited record
    edited_record = get_record(cursor, TEST_RECORD_NAME)
    assert edited_record, "Failed to retrieve the edited record"
    assert edited_record == TEST_PACKAGE_EDIT, "Record data does not match edited data"


def test_delete_record(cursor):
    # Delete the record
    delete_result = delete_record(cursor, TEST_RECORD_NAME)
    assert delete_result, "Record deletion failed"

    # Attempt to retrieve the deleted record
    deleted_record = get_record(cursor, TEST_RECORD_NAME)
    assert not deleted_record, "Record still exists after deletion"
"""
