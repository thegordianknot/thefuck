from subprocess import Popen, PIPE
import re
from thefuck.utils import which


def _get_bin(settings):
    return getattr(settings, 'command_not_found', '/usr/lib/command-not-found')


def _get_output(command, settings):
    name = command.script.split(' ')[command.script.startswith('sudo')]
    check_script = '{} {}'.format(_get_bin(settings), name)
    result = Popen(check_script, shell=True, stderr=PIPE)
    return result.stderr.read().decode()


def match(command, settings):
    if which('apt-get') and which(_get_bin(settings)):
        output = _get_output(command, settings)
        return "No command" in output and "from package" in output


def get_new_command(command, settings):
    output = _get_output(command, settings)
    broken_name = re.findall(r"No command '([^']*)' found",
                             output)[0]
    fixed_name = re.findall(r"Command '([^']*)' from package",
                            output)[0]
    return command.script.replace(broken_name, fixed_name, 1)