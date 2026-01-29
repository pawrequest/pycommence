from pycommence.dde.msgs import system


def test_client_system(pycmc_client):
    msg = system.status()
    res = pycmc_client.send_dde_message(msg)
    ...
