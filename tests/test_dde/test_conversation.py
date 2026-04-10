def test_get_item(test_client):
    # res = test_client_non_tutorial.item_read_dde('Hire', 'Little Gransden Charity Air - 24/08/2026 ref 32913')
    # res = test_client.item_read_dde('Hire', 'St Marys Hospice - 01/09/2026 ref 21554')
    res = test_client.item_read_dde('Contact', 'Musk.Elon')
    print(res)
