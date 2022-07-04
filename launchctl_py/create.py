#!/usr/bin/env python
# coding: utf-8

import json
import os
import shlex
import signal
import sys
import textwrap
from pathlib import Path


def keyboard_interrupt_handler(sig: int, _) -> None:
    """Handle keyboard interrupt."""
    print(f'\nKeyboardInterrupt (id: {sig}) has been caught...')
    print('Terminating the session gracefully...')
    sys.exit(1)


def create() -> None:
    """Create a new launchctl agent."""
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    HOME = Path.home()
    L_PATH = f'{HOME}/Library/Logs'
    domain = 'local'
    if os.getenv('DEFAULT_DOMAIN'):
        domain = os.getenv('DEFAULT_DOMAIN')

    agent_name = input('Agent Name (CamelCase): ')
    exec_bin = input('Executable binary full path: ')
    cmd_args = input('Program arguments: ')

    program_args = ''
    for arg in shlex.split(cmd_args):
        program_args += f'\t\t<string>{arg}</string>\n'

    plist_content = f'''\ <?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE 
    plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"> <plist version="1.0"> 
    <dict> <key>Label</key> <string>com.{domain}.{agent_name}</string> 

        <key>ProgramArguments</key>
        <array>
            <string>{exec_bin}</string>
    {program_args.rstrip()}
        </array>

        <key>RunAtLoad</key>
        <true/>

        <key>KeepAlive</key>
        <true/>

        <key>StandardErrorPath</key>
        <string>{L_PATH}/com.{domain}/com.{domain}.{agent_name}.err</string>

        <key>StandardOutPath</key>
        <string>{L_PATH}/com.{domain}/com.{domain}.{agent_name}.out</string>
    </dict>
    </plist>
    '''  # noqa: E501

    Path(f'{L_PATH}/com.{domain}').mkdir(exist_ok=True)

    plist_fpath = f'{HOME}/Library/LaunchAgents/com.{domain}.{agent_name}.plist'  # noqa: E501

    print('-' * 80)
    print(plist_content)
    print('-' * 80)

    ans = input('\n\nConfirm? (y/N) ')

    if ans.lower() not in ['y', 'yes']:
        sys.exit(1)

    with open(plist_fpath, 'w') as f:
        f.write(textwrap.dedent(plist_content))

    lagents = f'{Path.home()}/.lpyrc.json'

    if not Path(lagents).exists():
        with open(lagents, 'w') as j:
            json.dump([], j)

    with open(lagents, 'r+') as j:
        agents = json.load(j)
        agents.append(f'com.{domain}.{agent_name}')
        j.seek(0)
        json.dump(agents, j, indent=4)

    print('Run:')
    print(f'    sudo chown root:wheel {plist_fpath} && '
          f'sudo chmod o-w {plist_fpath} && '
          f'launchctl load {plist_fpath} && '
          f'launchctl list {Path(plist_fpath).stem} | grep \'"PID"\'')
