from pycommence.wrapper.cmc_db import CommenceWrapper


def test_it():
    # Your code that uses COM objects
    cmc = CommenceWrapper()
    conversation = cmc.get_conversation('ViewData')
    fdef = conversation.get_field_definition('Contact', 'firstName')
    ...
