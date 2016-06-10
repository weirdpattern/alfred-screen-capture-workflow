import os
import sys
import subprocess

from library import Workflow


def main(workflow):
    args = workflow.args

    query = ''
    if len(args) > 0:
        query = args.pop(0)

    count = 0
    if query != "$":

        if 'selection'.startswith(query.lower()):
            count += 1
            workflow.item('Selection', 'Take a screenshot of a selection',
                          lambda item: customize(item, workflow.resource('resources/selection.png'), 'selection',
                                                 autocomplete='Selection'))

        if 'window'.startswith(query.lower()):
            count += 1
            workflow.item('Window', 'Take a screenshot of an open window',
                          lambda item: customize(item, workflow.resource('resources/window.png'), 'window',
                                                 autocomplete='Window'))

        if 'full'.startswith(query.lower()) or 'screen'.startswith(query.lower()):
            count += 1
            workflow.item('Full Screen', 'Take a screenshot of the full screen',
                          lambda item: customize(item, workflow.resource('resources/full.png'), 'full',
                                                 autocomplete='Full Screen'))

        if 'interactive'.startswith(query.lower()):
            count += 1
            workflow.item('Interactive', '{space} to toggle between selection and window',
                          lambda item: customize(item, workflow.resource('resources/interactive.png'), 'interactive',
                                                 autocomplete='Interactive'))

        if 'timed'.startswith(query.lower()):
            count += 1
            workflow.item('Timed', 'Take a timed screenshot of the full screen',
                          lambda item: customize(item, workflow.resource('resources/timed.png'), 'timed',
                                                 autocomplete='Timed'))

    else:

        query = ''
        if len(args) > 0:
            query = args[0]
            if query == 'drop':
                return display_drop_menu(workflow, *args[1:])
            elif query == 'delay':
                return display_timer_menu(workflow, *args[1:])

        if 'drop'.startswith(query.lower()) or 'location'.startswith(query.lower()):
            count += 1
            workflow.item('Update the screenshot save location ',
                          'Current location -> {0}'.format(workflow.setting('workflow', 'drop')),
                          lambda item: customize(item, workflow.resource('resources/drop.png'), valid=False,
                                                 autocomplete="$ drop "))

        if 'timer'.startswith(query.lower()) or 'delay'.startswith(query.lower()):
            count += 1
            workflow.item('Update the timer delay',
                          'Current delay -> {0} seconds'.format(workflow.setting('workflow', 'delay')),
                          lambda item: customize(item, workflow.resource('resources/delay.png'), valid=False,
                                                 autocomplete="$ delay "))

    if count == 0:
        workflow.item('No match for {0}'.format(query), 'Click to clear your filter',
                      lambda item: customize(item, workflow.resource('resources/sad.png'), valid=False,
                                             autocomplete=''))

    workflow.feedback()
    return 0


def display_drop_menu(workflow, *args):
    if 'confirm' in args:
        drop = ' '.join(args[:-1])

        workflow.setting('workflow')['drop'] = drop
        workflow.settings.save()

        workflow.notification(workflow.name, 'The drop location was successfully updated')
        workflow.close()

        return 0
    elif len(args) > 0 and len(args[0]) > 0:
        drop = os.path.expanduser(' '.join(args))

        if os.path.exists(drop):
            workflow.item('Valid location',
                          'Please confirm you want to use "{0}"'.format(drop),
                          lambda item: customize(item, workflow.resource('resources/correct.png'), valid=False,
                                                 autocomplete='$ drop {0} confirm'.format(drop)))
        else:
            workflow.item('Invalid location',
                          'Location "{0}" does not exist'.format(drop),
                          lambda item: customize(item, workflow.resource('resources/incorrect.png'), valid=False,
                                                 autocomplete='$ drop {0}'.format(drop)))
    else:
        workflow.item('Please provide the new location', '',
                      lambda item: customize(item, workflow.resource('resources/input.png'), valid=False,
                                             autocomplete='$ drop '))

    workflow.feedback()
    return 0


def display_timer_menu(workflow, *args):
    if 'confirm' in args:
        delay = int(args[0])

        workflow.setting('workflow')['delay'] = delay
        workflow.settings.save()

        workflow.notification(workflow.name, 'The timer delay was successfully updated')
        workflow.close()

        return 0
    elif len(args) > 0 and len(args[0]) > 0:
        delay = str(args[0])

        if delay.isdigit():
            workflow.item('Valid delay',
                          'Please confirm you want to use {0}'.format(delay),
                          lambda item: customize(item, workflow.resource('resources/correct.png'), valid=False,
                                                 autocomplete='$ delay {0} confirm'.format(delay)))
        else:
            workflow.item('Invalid delay'.format(delay),
                          'Delay {0} is not a valid number'.format(delay),
                          lambda item: customize(item, workflow.resource('resources/incorrect.png'), valid=False,
                                                 autocomplete='$ delay {0}'.format(delay)))
    else:
        workflow.item('Please provide the timer delay', '',
                      lambda item: customize(item, workflow.resource('resources/input.png'), valid=False,
                                             autocomplete='$ delay '))

    workflow.feedback()
    return 0


def customize(item, icon, arg=None, valid=True, autocomplete=None):
    item.arg = arg
    item.icon = icon
    item.valid = valid
    item.autocomplete = autocomplete

    return item


def location():
    path = subprocess.Popen(['defaults', 'read', 'com.apple.screencapture'],
                            stdout=subprocess.PIPE).communicate()[0]

    path = path.split('"')
    return path[1]


if __name__ == '__main__':

    defaults = {
        'actionable': True,
        'help': 'https://github.com/weirdpattern/alfred-screen-capture-workflow',
        'workflow': {
            'delay': 5,
            'drop': location()
        },
        'update': {
            'enabled': True,
            'frequency': 7,
            'include-prereleases': False,
            'repository': {
                'github': {
                    'repository': 'alfred-screen-capture-workflow',
                    'username': 'weirdpattern'
                }
            }
        }
    }

    sys.exit(Workflow.run(main, Workflow(defaults)))
