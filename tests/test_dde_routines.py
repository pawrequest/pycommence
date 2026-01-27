from pycommence.client_dde.routines import fetch_category_field_definitions_dir


def test_rout(dde_server):
    res = fetch_category_field_definitions_dir('Contact', dde_server)
    ...