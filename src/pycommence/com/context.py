import contextlib

import comtypes
from loguru import logger


@contextlib.contextmanager
def com_multithreaded_context():
    """Context manager to initialise and uninitialise COM for multithreaded use."""
    initialized = False
    try:
        try:
            comtypes.CoInitializeEx(comtypes.COINIT_MULTITHREADED)
            logger.debug('COM initialised for multithreaded use')
            initialized = True
        except OSError as e:
            # -2147417850 == 0x80010106: Cannot change thread mode after it is set
            if getattr(e, 'winerror', None) != -2147417850:
                raise
            logger.debug('COM already initialised with different threading model')
        yield
    finally:
        if initialized:
            logger.debug('Uninitialising COM')
            comtypes.CoUninitialize()
