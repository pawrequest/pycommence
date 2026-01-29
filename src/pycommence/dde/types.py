from __future__ import annotations

import threading
from enum import StrEnum
from typing import Literal, Protocol, runtime_checkable

from pydantic import BaseModel, Field, model_validator

DDEParam = str | int | float | bool | None

DDETopicLiteral = Literal['ViewData', 'GetData', 'System']


class DDETopic(StrEnum):
    VIEW = 'ViewData'
    GET = 'GetData'
    SYSTEM = 'System'
    TUTORIAL = 'Tutorial'


class DDEKind(StrEnum):
    REQUEST = 'request'
    EXECUTE = 'execute'


class DDEMessageBase(BaseModel):
    func_name: str
    topic_literal: DDETopicLiteral = 'GetData'
    topic: DDETopic = DDETopic.GET
    kind: DDEKind = DDEKind.REQUEST
    params: list[DDEParam] = Field(default_factory=list[DDEParam])
    params_formatted: list = Field(default_factory=list, init=False, repr=False)
    returns: list[type] = Field(default_factory=list)

    @model_validator(mode='after')
    def format_params(self):
        if self.params is None:
            return self
        self.params_formatted = [_dde_format_param(p) for p in self.params]
        return self

    def __str__(self) -> str:
        args = ','.join(self.params_formatted)
        args_str = f'({args})' if self.params else ''
        res = f'[{self.func_name}{args_str}]'
        return res


class DDESystemRequest(DDEMessageBase):
    topic: DDETopic = DDETopic.SYSTEM

    def __str__(self) -> str:
        args = ','.join(self.params_formatted)
        args_str = f'({args})' if self.params else ''
        res = f'{self.func_name}{args_str}'
        return res


class DDERequestBase(DDEMessageBase):
    kind: DDEKind = DDEKind.REQUEST


class DDEExecuteBase(DDEMessageBase):
    kind: DDEKind = DDEKind.EXECUTE


class DDERequestGet(DDERequestBase):
    topic: DDETopic = DDETopic.GET


class DDERequestView(DDERequestBase):
    topic: DDETopic = DDETopic.VIEW


class DDEExecuteGet(DDEExecuteBase):
    topic: DDETopic = DDETopic.GET


class DDEExecuteView(DDEExecuteBase):
    topic: DDETopic = DDETopic.VIEW


def _dde_format_param(value: DDEParam) -> str:
    # None => blank placeholder
    if value is None:
        return ''
    # bool => yes/no (common in Commence docs)
    if isinstance(value, bool):
        return 'yes' if value else 'no'
    # numbers => as-is
    if isinstance(value, int | float):
        return str(value)
    # strings => quoted, internal quotes doubled
    if not isinstance(value, str):
        value = str(value)
    value = value.strip('"\'')
    return f'"{value}"'


@runtime_checkable
class DDEServerProtocol(Protocol):
    _lock: threading.Lock

    def send_message(self, msg: DDEMessageBase) -> str | list[str] | bool:
        ...

    def last_error(self) -> int:
        ...


EMPTY = 'empty'
