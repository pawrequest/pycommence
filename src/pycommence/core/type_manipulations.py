from typing import get_args, get_origin

from pydantic import BaseModel, create_model


def make_partial(model: type[BaseModel], cache=None) -> type[BaseModel]:
    if cache is None:
        cache = {}

    if model in cache:
        return cache[model]

    def optionalize(tp):
        origin = get_origin(tp)
        args = get_args(tp)

        # BaseModel → recurse
        if isinstance(tp, type) and issubclass(tp, BaseModel):
            return make_partial(tp, cache) | None

        # list[T], set[T], tuple[T], etc.
        if origin in (list, set, tuple):
            inner = tuple(optionalize(arg) for arg in args)
            return origin[inner] | None

        # dict[K, V]
        if origin is dict:
            k, v = args
            return dict[k, optionalize(v)] | None

        # Union[...] → optionalize each branch
        if origin is None and args:
            return (tuple(optionalize(arg) for arg in args)) | None

        # fallback
        return tp | None

    fields = {}

    for name, field in model.model_fields.items():
        new_type = optionalize(field.annotation)
        fields[name] = (new_type, None)

    partial = create_model(f'Partial{model.__name__}', __base__=BaseModel, **fields)
    cache[model] = partial
    return partial
