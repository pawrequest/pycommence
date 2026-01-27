from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger
def configure_loguru(
        level: str = 'DEBUG',
        log_file: Path | None = None,
):
    logger.debug('Configuring loguru logger')
    lvl = level.upper()
    logger.remove()
    if log_file:
        logger.add(log_file, rotation='1 day', delay=True, encoding='utf8', level='DEBUG')
    logger.add(sys.stderr, level=lvl, format=log_fmt_local_terminal)


def log_fmt_local_terminal(record) -> str:
    file_txt = f"{record['file'].path}:{record['line']}"
    category = record['extra'].get('category', 'General')
    category_txt = f'{category.title():<9}'
    lvltext = f'<lvl>{record['level']: <7}</lvl>'
    msg_txt = f'<lvl>{record['message']}</lvl>'
    msg_txt = msg_txt.replace('{', '{{').replace('}', '}}')
    return f'{file_txt} - {lvltext} {category_txt} | {msg_txt}\n'


def coloured(msg: str, colour: str) -> str:
    return f'<{colour}>{msg}</{colour}>'

