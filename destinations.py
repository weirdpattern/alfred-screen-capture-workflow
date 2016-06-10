import os
import re
import sys
import subprocess

from datetime import datetime
from library import Workflow


def main(workflow):
    args = workflow.args

    query = ''
    if len(args[0]) > 0:
        query = args[0]

    files = re.match(r'^(?:[0-9a-zA-Z_\-\\ ]+\.[0-9a-zA-Z]+)+$', query, re.I)
    directories = re.match(r'^~?/(?:[0-9a-zA-Z_\-\\/ ])*$', query, re.I)
    full_paths = re.match(r'^(~?/?(?:[0-9a-zA-Z_\-\\/ ])*)/((?:[0-9a-zA-Z_\-\\ ]+\.[0-9a-zA-Z]+)+)$', query, re.I)

    default = os.path.expanduser(workflow.setting('workflow', 'drop'))
    destination = os.path.join(default, random())

    if files:
        destination = os.path.join(default, query)
    elif directories:
        path = os.path.expanduser(query)
        destination = os.path.join(path, random()) if os.path.exists(path) else os.path.join(default, random())
    elif full_paths:
        path = os.path.expanduser(query)
        directory = os.path.expanduser(full_paths.group(1))
        destination = path if os.path.exists(directory) else os.path.join(default, full_paths.group(2))

    if not query:
        workflow.item('Clipboard', 'Copy to Clipboard',
                      lambda item: customize(item, 'clipboard', workflow.resource('resources/clipboard.png')))

        workflow.item('Send via Email', 'Send the screenshot via Email',
                      lambda item: customize(item, 'email:{0}'.format(os.path.join(default, random())),
                                             workflow.resource('resources/email.png')))

    workflow.item('Save to...', '-> {0}'.format(destination),
                  lambda item: customize(item, 'file:{0}'.format(destination), workflow.resource('resources/file.png')))

    workflow.feedback()
    return 0


def random():
    date = datetime.now()
    return 'screenshot-{0}{1}{2}{3}{4}.png'.format(date.year,
                                                   str(date.month).ljust(2, '0'),
                                                   str(date.day).ljust(2, '0'),
                                                   str(date.hour).ljust(2, '0'),
                                                   str(date.minute).ljust(2, '0'))


def customize(item, arg, icon):
    item.valid = 'yes'
    item.icon = icon
    item.arg = arg
    return item


if __name__ == '__main__':
    sys.exit(Workflow.run(main, Workflow()))