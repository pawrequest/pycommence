"""Tests for pycommence.core.type_manipulations"""

from pydantic import BaseModel

from pycommence.core.type_manipulations import make_partial


class SampleModel(BaseModel):
    name: str
    age: int
    email: str


class TestMakePartial:
    def test_all_fields_optional(self):
        Partial = make_partial(SampleModel)
        obj = Partial()  # all fields default to None
        assert obj.name is None
        assert obj.age is None

    def test_partial_accepts_values(self):
        Partial = make_partial(SampleModel)
        obj = Partial(name='Alice')
        assert obj.name == 'Alice'
        assert obj.age is None

    def test_name_has_prefix(self):
        Partial = make_partial(SampleModel)
        assert Partial.__name__.startswith('Partial')

    def test_cache(self):
        cache = {}
        p1 = make_partial(SampleModel, cache=cache)
        p2 = make_partial(SampleModel, cache=cache)
        assert p1 is p2
