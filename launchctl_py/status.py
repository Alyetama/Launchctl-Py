#!/usr/bin/env python
# coding: utf-8

import json
import os
import re
from pathlib import Path

from tabulate import tabulate


def status() -> str:
    """Get the status of the agents you created."""
    lagents_rc = f'{Path.home()}/.lpyrc'
    r, g, c, y, R = '\033[31m', '\033[32m', '\033[36m', '\033[33m', '\033[39m'

    if not Path(lagents_rc).exists():
        return f'{r}Could not find any custom agents...{R}'
    with open(lagents_rc, 'r') as j:
        agents = json.load(j)
        prefix = agents['prefix']

    table = []

    for agent in agents['agents']:
        out = os.popen(f'launchctl list {agent}').read()
        match = re.search(r'.+"PID".+', out)
        if match:
            pid = int(match[0].strip()[:-1].split('= ')[1])
            pid = f'{g}{pid}{R}'
        else:
            pid = f'\033[40m{r}DOWN{R}\033[49m'
        plist_path = f'{prefix}/{agent}.plist'.replace(str(Path.home()), '~')
        plist_path = f'{c}{plist_path}{R}'
        row = (plist_path, pid)
        table.append(row)

    headers = [f'{r}{x}{R}' for x in ['PATH', 'PID']]

    t = tabulate(table,
                 headers=headers,
                 tablefmt='pretty',
                 stralign='left',
                 showindex=True)
    return t
