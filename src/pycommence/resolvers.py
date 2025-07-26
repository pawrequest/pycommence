import functools
import typing as _t

from pycommence.cursor import CursorAPI
from pycommence.exceptions import PyCommenceNotFoundError


class HasCursors(_t.Protocol):
    csrs: dict[str, CursorAPI]


def get_csrname(self: HasCursors, csrname: str | None = None):
    if not csrname:
        if not self.csrs:
            raise PyCommenceNotFoundError('No cursor available')
        if len(self.csrs) > 1:
            raise ValueError('Multiple cursors available, specify csrname')
        csrname = next(iter(self.csrs.keys()))
    return csrname


def resolve_csrname(func):
    """Decorator to get csrname from first positional argument or kwargs['csrname'], or else the only cursor available, or else raise ValueError"""

    @functools.wraps(func)
    def wrapper(self: HasCursors, *args, **kwargs):
        if args:
            csrname = get_csrname(self, args[0])
            args = (csrname,) if len(args) == 1 else (csrname, *args[1:])
        elif 'csrname' in kwargs:
            if args:
                raise ValueError('Cannot use both positional and keyword csrname arguments')
            kwargs['csrname'] = get_csrname(self, kwargs['csrname'])
        else:
            kwargs['csrname'] = get_csrname(self)
        return func(self, *args, **kwargs)

    return wrapper


def resolve_row_id(func):
    """Decorator to get row_id from kwargs, or else get pk and cursornames from kwargs, and use self.cursor's pk_to_id method."""

    @functools.wraps(func)
    def wrapper(self: HasCursors, *args, **kwargs):
        row_id = kwargs.get('row_id')
        if not row_id:
            pk = kwargs.get('pk')
            if not pk:
                raise ValueError('Either row_id or pk must be provided')
            csrname = kwargs.get('csrname') or next(iter(self.csrs.keys())) if self.csrs else None
            if not csrname:
                raise PyCommenceNotFoundError('No cursor available to convert pk to id')
            row_id = self.csrs[csrname].pk_to_id(pk)
            kwargs['row_id'] = row_id

        return func(self, *args, **kwargs)

    return wrapper
