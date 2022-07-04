#!/usr/bin/env python
# coding: utf-8

import json
import os
import re
from pathlib import Path

from tabulate import tabulate


def status() -> str:
    """Get the status of the agents you created."""
    r, g, c, y, R = '\033[31m', '\033[32m', '\033[36m', '\033[33m', '\033[39m'

    if not Path(f'{Path.home()}/.lpyrc.json').exists():
        return f'{r}No custom agents found.{R}'
    with open(f'{Path.home()}/.lpyrc.json', 'r') as j:
        agents = json.load(j)

    table = []

    for agent in agents:
        out = os.popen(f'launchctl list {agent}').read()
        match = re.search(r'.+"PID".+', out)
        pid = int(match[0].strip()[:-1].split('= ')[1])
        pid = f'{g}{pid}{R}'
        LAGENTS = f'~/Library/LaunchAgents'
        if os.getenv('LAGENTS'):
            LAGENTS = '$LAGENTS'
        plist_path = f'"{LAGENTS}/{agent}.plist"'
        plist_path = f'{c}{plist_path}{R}'
        label = f'{y}{agent.split(".")[-1]}{R}'
        row = (label, plist_path, pid)
        table.append(row)

    headers = [f'{r}{x}{R}' for x in ['LABEL', 'PATH', 'PID']]

    t = tabulate(table,
                 headers=headers,
                 tablefmt='pretty',
                 stralign='left',
                 showindex=True)
    return t
