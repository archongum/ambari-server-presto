# -*- coding: utf-8 -*-
from resource_management.libraries.script.script import Script
from resource_management.core.exceptions import ClientComponentHasNoStatus


class Cli(Script):
    def install(self, env):
        from common import presto_cli_file
        from common_func import exec_command

        try:
            exec_command('cp -r {1} {0}/presto-cli'.format('/usr/bin', presto_cli_file))
            exec_command('chmod +x {0}/presto-cli'.format('/usr/bin'))
        except BaseException:
            pass

    def status(self, env):
        raise ClientComponentHasNoStatus()


if __name__ == '__main__':
    Cli().execute()
