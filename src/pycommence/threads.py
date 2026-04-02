import contextlib
import threading

from loguru import logger
from pythoncom import CoInitializeEx, CoUninitialize

from pycommence.icommence.const import ComAlreadyInitDifferentMode
from pycommence.pycommence_options import get_options

THREAD_MODEL = get_options().thread_model


@contextlib.contextmanager
def com_context(mode: int = THREAD_MODEL):
    """Context manager to initialise and uninitialise COM for multithreaded use."""
    initialized = False
    try:
        thread_id = threading.get_ident()
        try:
            CoInitializeEx(mode)
            logger.debug(
                f'Thread {thread_id} COM initialised for {'COINIT_MULTITHREADED' if mode == 0 else 'COINIT_APARTMENTTHREADED' if mode == 2 else 'unknown'} use'
            )
            initialized = True
        except OSError as e:
            # -2147417850 == 0x80010106: Cannot change thread mode after it is set
            if getattr(e, 'winerror', None) != ComAlreadyInitDifferentMode:
                raise
            logger.warning('DDEServer fixture running in thread ')
            logger.debug(f'Thread {thread_id} COM already initialised with different threading model')
        except Exception as e:
            logger.error(f'Error initialising COM in thread {thread_id}: {e}')
            raise
        yield
    finally:
        if initialized:
            logger.debug('Uninitialising COM')
            CoUninitialize()
