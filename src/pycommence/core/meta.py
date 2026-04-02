from abc import ABC
from typing import ClassVar, Literal, cast

from loguru import logger
from pydantic import BaseModel, ConfigDict

from pycommence.core.fields import CmcDefsDict

TABLE_TYPE_REGISTER: dict[str, type['CommenceTable']] = {}
GENERATED_TABLE_TYPE_REGISTER: dict[str, type['CommenceTableGenerated']] = {}

FetchMode = Literal['manual', 'auto', 'all']
HandleMissing = Literal['raise', 'ignore', 'generate']


def register_table(cls: 'type[CommenceTable] | type[CommenceTableGenerated]'):
    if issubclass(cls, CommenceTableGenerated):
        logger.debug(f'Registering generated table model: {cls.__name__}')
        GENERATED_TABLE_TYPE_REGISTER[str(cls.__name__)] = cls
    elif issubclass(cls, CommenceTable):
        logger.debug(f'Registering table model: {cls.category}')
        TABLE_TYPE_REGISTER[str(cls.category)] = cls


def get_table_type(
    table_name: str, mode: FetchMode = 'manual', missing: HandleMissing = 'ignore'
) -> type['CommenceTableGenerated'] | type['CommenceTable'] | None:
    register = None
    match mode:
        case 'auto':
            register = GENERATED_TABLE_TYPE_REGISTER
        case 'manual':
            register = TABLE_TYPE_REGISTER
        case 'all':
            register = {**TABLE_TYPE_REGISTER, **GENERATED_TABLE_TYPE_REGISTER}
        case _:
            raise ValueError(f'Invalid mode: {mode}')
    if res := register.get(table_name):
        return res
    if missing == 'raise':
        raise KeyError(f'No registered table model for: {table_name} in mode: {mode}')
    # if missing == 'generate':
    #     logger.debug(f'Generating table model for missing table: {table_name}')
    #     return generate_table_pydantic_model(table_name, table_name)

    return None


class CommenceTableGenerated(BaseModel, ABC):
    model_config = ConfigDict(extra='allow')

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        register_table(cls)


class CommenceTable(BaseModel, ABC):
    model_config = ConfigDict(extra='ignore')
    category: ClassVar[str]
    name_field: ClassVar[str | None] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if getattr(cls, '__abstractmethods__', False):
            logger.warning(f'SURPRISE!!! Not registering abstract table model: {cls.__name__}')
            return
        if not getattr(cls, 'category', None):
            raise TypeError(f'{cls.__name__} must define category class variable')
        register_table(cls)


def generate_table_pydantic_model(
    name: str,
    category: str,
    field_def_dict: CmcDefsDict = None,
) -> type[CommenceTableGenerated]:
    """Dynamically generate a CommenceTable subclass."""
    if existing_type := get_table_type(name, mode='auto'):
        logger.debug(f'Table class {name} already exists, reusing.')
        return existing_type
    defs_dict = field_def_dict or CmcDefsDict()
    annotations = defs_dict.py_types_dict()
    annotations['category'] = ClassVar[str]
    annotations['name_field'] = ClassVar[str]

    class_dict = {
        '__module__': __name__,
        '__qualname__': name,
        '__annotations__': annotations,
        'category': category,
        'name_field': defs_dict.name_field(error='ignore'),
    }
    for k in field_def_dict.keys():
        class_dict[k] = None

    logger.debug(f'Generating table class {name}.')
    table_class = type(name, (CommenceTableGenerated,), class_dict)
    table_class = cast(type[CommenceTableGenerated], table_class)
    register_table(table_class)
    return table_class
