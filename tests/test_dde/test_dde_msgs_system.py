import inspect

from pycommence.dde import DDETopic
from pycommence.dde.msgs import system as system_msgs

TESTCOUNT = 1

def test_all_system_funcs(dde_server, caplog):
    dde_server._connect_topic(DDETopic.SYSTEM)
    dde_server.options.strip_strs = True
    with caplog.at_level('DEBUG'):
        functions = (func for name, func in inspect.getmembers(system_msgs, inspect.isfunction))

        for func in functions:
            msg = func()
            response = dde_server.send_message(msg)
            assert response is not None, f"Response for {func.__name__} is None"
            # sleep(2)  # To avoid overwhelming the DDE server
    print("\nCaptured Logs:")
    for record in caplog.records:
        print(f"{record.levelname}: {record.message}")

