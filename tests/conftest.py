import random

import pytest

from pycommence import api
import sample_data


@pytest.fixture
def hire_csr():
    with api.csr_context("Hire") as csr:
        yield csr


@pytest.fixture
def contact_csr():
    with api.csr_context("Contact") as csr:
        yield csr


@pytest.fixture
def sale_csr():
    with api.csr_context("Sale") as csr:
        yield csr


@pytest.fixture(scope="session")
def random_hire_record():
    rec = random.choice(sample_data.hires)
    return rec
