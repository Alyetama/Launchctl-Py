#!/usr/bin/env python
# coding: utf-8

import os
import shlex
import signal
import sys
import textwrap
from pathlib import Path


def keyboard_interrupt_handler(sig: int, _) -> None:
    print(f'\nKeyboardInterrupt (id: {sig}) has been caught...')
    print('Terminating the session gracefully...')
    sys.exit(1)


def main():
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)

    HOME = Path.home()
    entity = os.environ['DEFAULT_ENTITY']

    agent_name = input('Agent Name (CamelCase): ')
    exec_bin = input('Executable binary full path: ')
    cmd_args = input('Program arguments: ')

    program_args = ''
    for arg in shlex.split(cmd_args):
        program_args += f'\t\t<string>{arg}</string>\n'

    plist_content = f'''\
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.{entity}.{agent_name}</string>

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
        <string>{HOME}/Library/Logs/com.{entity}/com.{entity}.{agent_name}.err</string>

        <key>StandardOutPath</key>
        <string>{HOME}/Library/Logs/com.{entity}/com.{entity}.{agent_name}.out</string>
    </dict>
    </plist>
    '''

    Path(f'/Users/Felis.catus/Library/Logs/com.{entity}').mkdir(exist_ok=True)

    plist_fpath = f'{HOME}/Library/LaunchAgents/com.{entity}.{agent_name}.plist'

    print('-' * 80)
    print(plist_content)
    print('-' * 80)

    ans = input('\n\nConfirm? (y/N) ')

    if ans.lower() not in ['y', 'yes']:
        sys.exit(1)

    with open(plist_fpath, 'w') as f:
        f.write(textwrap.dedent(plist_content))

    print('Run:')
    print(f'    sudo chown root:wheel {plist_fpath} && '
        f'sudo chmod o-w {plist_fpath} && '
        f'launchctl load {plist_fpath} && '
        f'launchctl list {Path(plist_fpath).stem} | grep \'"PID"\'')


if __name__ == '__main__':
    main()
