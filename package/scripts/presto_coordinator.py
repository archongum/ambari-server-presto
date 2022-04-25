# -*- coding: utf-8 -*-
from resource_management.libraries.script.script import Script
from resource_management.core.exceptions import ComponentIsNotRunning

from common_func import exec_command


class Coordinator(Script):
    def install(self, env):
        from common import presto_install_dir, presto_plugin_dir, presto_launcher_script, \
            java_home, presto_tar_file
        from common_func import init_dirs

        # 0: presto_tar_file; 1: presto_install_dir; 2: bin or lib or plugin; 3: strip-components
        tar_pattern = 'tar -xvf {0} -C {1} --strip-components={3} `tar -tf {0} | head -n 1`{2}'
        # cleanup
        exec_command('rm -rf {0}'.format(presto_install_dir))
        # init dirs
        init_dirs()
        # install and set java_home
        exec_command(tar_pattern.format(presto_tar_file, presto_install_dir, '*', 1))
        exec_command('sed -i "2iexport JAVA_HOME={0}" {1}'.format(java_home, presto_launcher_script))
        exec_command('sed -i "3iexport PATH=\$JAVA_HOME/bin:\$PATH" {0}'.format(presto_launcher_script))
        # config
        self.configure(env)

    def stop(self, env):
        from common import presto_launcher_script

        exec_command('{0} stop'.format(presto_launcher_script))

    def start(self, env):
        from common import presto_launcher_script, config_properties, host_info
        from presto_client import PrestoClient, smoketest_presto

        self.configure(env)
        exec_command('{0} start'.format(presto_launcher_script))
        # test
        if 'presto_worker_hosts' in host_info.keys():
            all_hosts = host_info['presto_worker_hosts'] + \
                        host_info['presto_coordinator_hosts']
        else:
            all_hosts = host_info['presto_coordinator_hosts']
        # use Set, coordinator could be worker
        all_hosts = set(all_hosts)
        smoketest_presto(PrestoClient('localhost', 'root', config_properties['http-server.http.port']), all_hosts)

    def status(self, env):
        from common import presto_launcher_script

        stdout = exec_command('{0} status'.format(presto_launcher_script))
        if 'Not running' in stdout:
            raise ComponentIsNotRunning(stdout)

    def configure(self, env):
        import os
        from common import node_properties, jvm_config, config_properties, \
            presto_etc_dir, memory_configs
        from common_func import create_connectors, delete_connectors

        key_val_template = '{0}={1}\n'
        hostname = exec_command('hostname')

        with open(os.path.join(presto_etc_dir, 'node.properties'), 'w') as f:
            for key, value in node_properties.iteritems():
                f.write(key_val_template.format(key, value))
            f.write(key_val_template.format('node.id', hostname))

        with open(os.path.join(presto_etc_dir, 'jvm.config'), 'w') as f:
            f.write(jvm_config['jvm.config'])

        with open(os.path.join(presto_etc_dir, 'config.properties'), 'w') as f:
            for key, value in config_properties.iteritems():
                if key in memory_configs:
                    value += 'MB'
                f.write(key_val_template.format(key, value))
            f.write(key_val_template.format('coordinator', 'true'))
            f.write(key_val_template.format('discovery-server.enabled', 'true'))

        create_connectors()
        delete_connectors()
        # This is a separate call because we always want the tpch connector to
        # be available because it is used to smoketest the installation.
        # create_connectors(node_properties, "{'tpch': ['connector.name=tpch']}")


if __name__ == '__main__':
    Coordinator().execute()
