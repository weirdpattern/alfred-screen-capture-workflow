import os
import sys
import subprocess

from library import Workflow


def main(workflow):
    mode = workflow.args[0]
    destination = workflow.args[1].split(':') if workflow.args[1].find(':') > -1 else [workflow.args[1], None]

    command = ['screencapture']
    command.extend(arguments(workflow, mode, destination[0]).split(' '))

    if destination[1]:
        command.append(os.path.expanduser(destination[1]))

    if subprocess.call(command) != 0:
        sys.stdout.write('Oops, something went wrong with your screenshot. Are you using a valid path?')
        return 1

    sys.stdout.write('Screenshot taken and sent to {0}'.format(
        destination[1] if destination[0] == 'file' else destination[0])
    )

    return 0


def arguments(workflow, mode, destination):
    options = '-x'
    if mode == 'selection':
        options += 'sm'
    elif mode == 'window':
        options += 'wmo'
    elif mode == 'interactive':
        options += 'iW'

    if destination == 'clipboard':
        options += 'c'
    elif destination == 'email':
        options += 'M'

    if mode == 'timed':
        options += ' -T {0}'.format(workflow.setting('workflow', 'delay'))

    return options


if __name__ == '__main__':
    sys.exit(Workflow.run(main, Workflow()))
