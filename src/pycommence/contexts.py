import contextlib
import typing as _t
from functools import partial
from typing import Any, TYPE_CHECKING

import win32ui  # noqa
import dde

if TYPE_CHECKING:
    from _win32typing import PyDDEConv
else:
    PyDDEConv = Any  # type: ignore
from comtypes import CoInitialize, CoUninitialize
from loguru import logger

from pycommence import PyCommence


@contextlib.contextmanager
def pycommence_context(*csrnames: str) -> _t.Generator[PyCommence, None, None]:
    """Context manager for PyCommence with optional cursors"""
    CoInitialize()
    pyc = PyCommence()
    for csrname in csrnames:
        pyc.set_csr(csrname)
    yield pyc
    CoUninitialize()


@contextlib.contextmanager
def conversaton_context_no_Icommence(application, topic) -> _t.Generator[PyDDEConv, Any, None]:
    # Create a DDE client
    dde_client = None
    conversation: PyDDEConv = None  # type: ignore
    try:
        if dde_client is None:
            logger.debug('Creating new DDE client')
            dde_client = dde.CreateServer()
            dde_client.Create('MyDDEClient')
        if conversation is None:
            logger.debug('Creating new DDE conversation')
            conversation = dde.CreateConversation(dde_client)
            conversation.ConnectTo(application, topic)
            logger.debug(f'Established DDE conversation to {application}:{topic}')
        yield conversation
    except Exception as e:
        if isinstance(e, dde.error):
            logger.error(f'Error during DDE conversation setup or use {application=} {topic=}: {e}')
        if conversation:
            yield conversation
        else:
            raise
    finally:
        logger.info('Closing DDE conversation')
        dde_client.Shutdown()


pycommence_conversation_context = partial(conversaton_context_no_Icommence, 'Commence')
