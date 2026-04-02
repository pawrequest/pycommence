from loguru import logger
from pydantic import BaseModel


def alias_lookup(cls: type[BaseModel], field_name: str) -> str:
    try:
        return cls.model_fields[field_name].alias
    except KeyError:
        logger.warning(f'Alias for {field_name} not found in model {cls.__name__}. Returning field name.')
        return field_name
