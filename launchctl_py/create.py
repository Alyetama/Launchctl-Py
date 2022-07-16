#!/usr/bin/env python
# coding: utf-8

import json
import shlex
import signal
import sys
import textwrap
from pathlib import Path
from typing import Optional


def keyboard_interrupt_handler(sig: int, _) -> None:
    """Handle keyboard interrupt."""
    print(f'\nKeyboardInterrupt (id: {sig}) has been caught...')
    print('Terminating the session gracefully...')
    sys.exit(1)


def create(noninteractive: bool = False,
           agent_name: Optional[str] = None,
           exec_bin: Optional[str] = None,
           cmd_args: Optional[str] = None) -> None:
    """Create a new launchctl agent."""
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    HOME = Path.home()

    lagents_rc = f'{Path.home()}/.lpyrc'

    if not Path(lagents_rc).exists():
        with open(lagents_rc, 'w') as j:
            LAGENTS_PREFIX = f'{HOME}/Library/LaunchAgents'
            DOMAIN = 'local'
            L_PATH = f'{HOME}/Library/Logs'
            json.dump(
                {
                    'prefix': LAGENTS_PREFIX,
                    'domain': DOMAIN,
                    'logs': L_PATH,
                    'agents': []
                }, j)
    else:
        with open(lagents_rc) as j:
            lagents_rc_content = json.load(j)
            LAGENTS_PREFIX = lagents_rc_content['prefix']
            DOMAIN = lagents_rc_content['domain']
            L_PATH = lagents_rc_content['logs']

    if not noninteractive:
        agent_name = input('Agent Name (CamelCase): ')
        exec_bin = input('Executable binary full path: ')
        cmd_args = input('Program arguments: ')

    program_args = ''
    for n, arg in enumerate(shlex.split(cmd_args)):
        if n == 0:
            program_args += f'\t\t<string>{arg}</string>\n'
        else:
            program_args += f'\t\t\t<string>{arg}</string>\n'

    plist_content = f'''\
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"> <plist version="1.0"> 
    <dict>
        <key>Label</key>
        <string>com.{DOMAIN}.{agent_name}</string> 

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
        <string>{L_PATH}/com.{DOMAIN}/com.{DOMAIN}.{agent_name}.err</string>

        <key>StandardOutPath</key>
        <string>{L_PATH}/com.{DOMAIN}/com.{DOMAIN}.{agent_name}.out</string>
    </dict>
    </plist>
    '''  # noqa: E501
    plist_content = textwrap.dedent(plist_content)

    Path(f'{L_PATH}/com.{DOMAIN}').mkdir(exist_ok=True)

    plist_fpath = f'{LAGENTS_PREFIX}/com.{DOMAIN}.{agent_name}.plist'

    print('-' * 80)
    print(plist_content)
    print('-' * 80)

    ans = input('\n\nConfirm? (y/N) ')

    if ans.lower() not in ['y', 'yes']:
        sys.exit(1)

    with open(plist_fpath, 'w') as f:
        f.write(plist_content)

    with open(lagents_rc, 'r+') as j:
        agents = json.load(j)
        entry = f'com.{DOMAIN}.{agent_name}'
        if entry not in agents['agents']:
            agents['agents'].append(entry)
            j.seek(0)
            json.dump(agents, j, indent=4)

    print('Run:')
    print(f'    sudo chown root:wheel {plist_fpath} && '
          f'sudo chmod o-w {plist_fpath} && '
          f'launchctl load {plist_fpath} && '
          f'launchctl list {Path(plist_fpath).stem} | grep \'"PID"\'')
