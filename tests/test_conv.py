import datetime
import pathlib
from decimal import Decimal
from enum import Enum
import typing as _t

import pydantic as _p
import pythoncom

from pycommence.wrapper.cmc_db import Cmc



def test_it():
    # Your code that uses COM objects
    cmc = Cmc()
    conversation = cmc.get_conversation('ViewData')
    fdef = conversation.get_field_definition('Contact', 'firstName')
    ...

