from typing import Optional, Sequence, Union

from pydantic import BaseModel, Field, model_validator

from pycommence.wrapper.conversation_wrapper import DDEKind, DDETopic

DDEParam = Optional[Union[str, int, float, bool]]


class DDEMessage(BaseModel):
    func_name: str
    topic: DDETopic = DDETopic.GET
    kind: DDEKind = DDEKind.REQUEST
    params: list[DDEParam] = Field(default_factory=list[DDEParam])
    parms_formatted: list = Field(default_factory=list, init=False, repr=False)

    @model_validator(mode='after')
    def format_params(self):
        self.parms_formatted = [_dde_format_param(p) for p in self.params]
        return self

    @property
    def commence_format(self) -> str:
        if not self.params:
            return f"[{self.func_name}]"
        inner = ",".join(self.parms_formatted)
        res = f"[{self.func_name}({inner})]"
        return res


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
    return f'"{value}"'


def _dde_format_function(func_name: str, params: Sequence[DDEParam] = None) -> str:
    if not params:
        return f"[{func_name}]"  # todo these dont work? only system topic without args?
    inner = ",".join(_dde_format_param(p) for p in params)
    return f"[{func_name}({inner})]"
