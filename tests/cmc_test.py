from src.commence_py.commence import CmcContext

with CmcContext() as cmc:
    hire = cmc.hires_by_customer('Test')[0]
    assert hire['To Customer'] == 'Test'
    ...
