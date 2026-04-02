import inspect

from pycommence.dde.msgs import system as system_msgs

TESTCOUNT = 1


def test_all_system_funcs(pycmc_client):
    system_msg_funcs = (func for name, func in inspect.getmembers(system_msgs, inspect.isfunction))
    for func in system_msg_funcs:
        msg = func()
        res = pycmc_client.send_dde_message(msg)
        assert res is not None, f'Response for {func.__name__} is None'
    print('\nCaptured Logs:')


# def test_all_system_funcs1(pycmc_client, caplog):
#     pycmc_client.options.strip_strs = True
#     with caplog.at_level('DEBUG'):
#         system_msg_funcs = (func for name, func in inspect.getmembers(system_msgs, inspect.isfunction))
#
#         for func in system_msg_funcs:
#             msg = func()
#             res = pycmc_client.send_dde_message(msg)
#             assert res is not None, f'Response for {func.__name__} is None'
#     print('\nCaptured Logs:')
#     for record in caplog.records:
#         print(f'{record.levelname}: {record.message}')
