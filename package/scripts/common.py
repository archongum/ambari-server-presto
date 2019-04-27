# -*- coding: utf-8 -*-
import os
try:
    import ConfigParser as cp
except ImportError:
    import configparser as cp
from common_func import exec_command, kv_print

from resource_management.libraries.script.script import Script

# Read config
package_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config = cp.ConfigParser()
config.read(os.path.join(package_dir, 'config.ini'))

# JAVA_HOME
java_home = config.get('other', 'java_home')
kv_print('java_home', java_home)

# Tarball file
presto_tar_file_0 = config.get('download', 'presto_tar_file')
presto_tar_file = exec_command('ls {0}'.format(presto_tar_file_0))
# presto_tar_name = presto_tar_file.split('/')[-1]

presto_cli_file_0 = config.get('download', 'presto_cli_file')
presto_cli_file = exec_command('ls {0}'.format(presto_cli_file_0))
kv_print('presto_tar_file', presto_tar_file)
kv_print('presto_cli_file', presto_cli_file)


# Config object that holds the configurations declared in the config xml file
script_config = Script.get_config()

host_info = script_config['clusterHostInfo']
host_level_params = script_config['hostLevelParams']
kv_print('host_info', host_info)
kv_print('host_level_params', host_level_params)


# Config files
node_properties = script_config['configurations']['node.properties']
jvm_config = script_config['configurations']['jvm.config']
config_properties = script_config['configurations']['config.properties']
connectors_properties = script_config['configurations']['connectors.properties']

connectors_to_add = connectors_properties['connectors.to.add']
connectors_to_delete = connectors_properties['connectors.to.delete']

# Some constants
presto_install_dir = '/usr/lib/presto'
presto_bin_dir = presto_install_dir + '/bin'
presto_etc_dir = '/etc/presto'
presto_etc_link = presto_install_dir + '/etc'
presto_lib_dir = presto_install_dir + '/lib'
presto_plugin_dir = node_properties['plugin.dir']
presto_catalog_dir = node_properties['catalog.config-dir']

need_init_dirs = [
    presto_install_dir, presto_etc_dir, presto_plugin_dir, presto_catalog_dir
]

presto_launcher_script = presto_bin_dir + '/launcher'

memory_configs = [
    'memory.heap-headroom-per-node',
    'query.max-memory',
    'query.max-total-memory',
    'query.max-memory-per-node',
    'query.max-total-memory-per-node'
]
