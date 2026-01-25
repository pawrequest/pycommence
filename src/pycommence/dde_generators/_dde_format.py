from typing import Optional, Sequence, Union

DDEParam = Optional[Union[str, int, float, bool]]


def _dde_escape_param(value: str) -> str:
    # Commence DDE rule: to embed a double quote in a parameter, use two double quotes.
    return value.replace('"', '""')


def _dde_format_param(value: DDEParam) -> str:
    # None => blank placeholder
    if value is None:
        return ""
    # bool => yes/no (common in Commence docs)
    if isinstance(value, bool):
        return "yes" if value else "no"
    # numbers => as-is
    if isinstance(value, (int, float)):
        return str(value)
    # strings => quoted, internal quotes doubled
    if not isinstance(value, str):
        value = str(value)
    return f'"{_dde_escape_param(value)}"'


def _dde_format_function(func_name: str, params: Sequence[DDEParam] = None) -> str:
    if not params:
        return f"[{func_name}]"  # todo these dont work? only system topic without args?
    inner = ",".join(_dde_format_param(p) for p in params)
    return f"[{func_name}({inner})]"
