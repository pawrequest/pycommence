from __future__ import annotations

from pydantic.alias_generators import to_snake
from sqlmodel import Session

from pycommence.models import CmcModelIn
from pycommence.models.cmc_models import CmcModelRaw

from pydantic._internal._model_construction import ModelMetaclass

def sub_model_from_cmc_db[T](
        cls: type[T],
        cmc_obj: CmcModelRaw | CmcModelIn,
        session: Session,
        # parent_id: int,
        *,
        prepend: str = ''
) -> T:
    # ob_dict = {
    #     attr: getattr(cmc_obj, f'{cls}.{prepend}{attr}', None) for attr in cls.__fields__
    # }
    ob_dict = {}
    for attr in cls.model_fields:
        valstr = to_snake(f'{cls.__name__}.{prepend}{attr}')
        val = getattr(cmc_obj, valstr, None)
        if isinstance(val, ModelMetaclass):
            val = sub_model_from_cmc_db(val, cmc_obj, session)
        if val is not None:
            ob_dict[attr] = val
    db_model_instance = cls(
        **ob_dict,
        # hire_id=parent_id
    )
    session.add(db_model_instance)
    session.commit()
    session.refresh(db_model_instance)
    return db_model_instance
