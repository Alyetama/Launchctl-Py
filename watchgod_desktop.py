#!/usr/bin/env python
# coding: utf-8

import asyncio
import os
import shutil
import signal
import sys
from pathlib import Path

from loguru import logger
from watchfiles import awatch

#-------------------------------------------------------------------------------
HOME = Path.home()
background_tasks = set()

conditions = {
    'screenshot': ('screenshot', 60, f'{HOME}/Pictures'),
    'tmp_py': ('temporary .py file', (60 * 60) * 24, f'{HOME}/Documents'),
    'multimedia': ('multimedia file', 60 * 60, f'{HOME}/Pictures')
}
#-------------------------------------------------------------------------------


class Condition:

    def __init__(self, path, name, sleep, dest):
        self.name = name
        self.path = path
        self.sleep = sleep
        self.dest = dest


def keyboard_interrupt_handler(sig: int, _) -> None:
    logger.warning(f'KeyboardInterrupt (id: {sig}) has been caught...')
    logger.info('Terminating the session gracefully...')
    sys.exit(1)


async def process(c):
    logger.debug(f'Detected a {c.name}: "{Path(c.path).name}"')
    await asyncio.sleep(c.sleep)
    try:
        shutil.move(c.path, c.dest)
        logger.debug(f'Moved: "{Path(c.path).name}" to "{c.dest}"')
    except FileNotFoundError:
        pass
    

async def main():
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    async for changes in awatch(f'{HOME}/Desktop'):
        for change in changes:
            if change[0].value != 1:
                continue
            c = None
            path = Path(change[1])
            if path.stem.startswith('Screen Shot'):
                c = Condition(path, *conditions['screenshot'])
            elif path.suffix == '.py' and path.stem.startswith('_'):
                c = Condition(path, *conditions['tmp_py'])
            elif path.suffix.lower() in [
                    '.jpg', '.jpeg', '.png', '.gif', '.mp4'
            ] and 'Screen Shot' not in path.stem:
                c = Condition(path, *conditions['multimedia'])

            if c:
                task = asyncio.create_task(process(c))
                background_tasks.add(task)
                task.add_done_callback(background_tasks.discard)


if __name__ == '__main__':
    entity = os.environ['DEFAULT_ENTITY']
    asyncio.run(main())
