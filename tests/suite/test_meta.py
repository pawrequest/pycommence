"""Tests for pycommence.core.meta"""

import pytest

from pycommence.core.fields import CmcDataType, CmcDefsDict, CmcFieldDefinition
from pycommence.core.meta import (
    _GENERATED_TABLE_TYPE_REGISTER,
    CommenceTable,
    CommenceTableGenerated,
    generate_table_pydantic_model,
    get_table_type,
    registered_table_models,
)


class TestGetTableType:
    def test_missing_ignore(self):
        result = get_table_type('__NONEXISTENT__', mode='manual', missing='ignore')
        assert result is None

    def test_missing_raise(self):
        with pytest.raises(KeyError):
            get_table_type('__NONEXISTENT__', mode='manual', missing='raise')

    def test_invalid_mode(self):
        with pytest.raises(ValueError):
            get_table_type('X', mode='INVALID')


class TestGenerateTablePydanticModel:
    def test_generates_model(self):
        defs = CmcDefsDict()
        defs['myName'] = CmcFieldDefinition(
            type=CmcDataType.lookup_datatype('NAME'),
            combobox=False,
            shared=False,
            mandatory=False,
            recurring=False,
            max_chars=100,
        )
        defs['myCity'] = CmcFieldDefinition(
            type=CmcDataType.lookup_datatype('TEXT'),
            combobox=False,
            shared=False,
            mandatory=False,
            recurring=False,
            max_chars=200,
        )
        model_cls = generate_table_pydantic_model(
            '__TestGen__',
            '__TestGen__',
            field_def_dict=defs,
        )
        assert issubclass(model_cls, CommenceTableGenerated)
        # cleanup
        _GENERATED_TABLE_TYPE_REGISTER.pop('__TestGen__', None)

    def test_reuses_existing(self):
        defs = CmcDefsDict()
        defs['x'] = CmcFieldDefinition(
            type=CmcDataType.lookup_datatype('TEXT'),
            combobox=False,
            shared=False,
            mandatory=False,
            recurring=False,
            max_chars=50,
        )
        m1 = generate_table_pydantic_model('__TestReuse__', '__TestReuse__', defs)
        m2 = generate_table_pydantic_model('__TestReuse__', '__TestReuse__', defs)
        assert m1 is m2
        _GENERATED_TABLE_TYPE_REGISTER.pop('__TestReuse__', None)


class TestCommenceTable:
    def test_subclass_must_have_category(self):
        with pytest.raises(TypeError):

            class BadTable(CommenceTable):
                name: str


class TestRegisteredTableModels:
    def test_returns_list(self):
        assert isinstance(registered_table_models('manual'), list)
        assert isinstance(registered_table_models('auto'), list)
        assert isinstance(registered_table_models('all'), list)
