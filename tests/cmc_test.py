from pycommence import api

rec_name = '_xcga fake hire'
package = {'To Customer': 'Test', 'Delivery Contact': 'a contact', }

db = api.CmcDB()
curs = db.get_cursor(name='Hire')
if api.filter_by_name(curs, rec_name):
    delet = api.delete_record(curs, rec_name)
    curs = db.get_cursor(name='Hire')
add = api.add_record(curs, record_name=rec_name, package=package)
...
curs = db.get_cursor(name='Hire')
del_row = api.delete_record(curs, record_name=rec_name)
...



