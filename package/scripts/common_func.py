import subprocess
import json
import os


def kv_print(k, v):
    print('---- [kv_print] {0}={1}'.format(k, v))
    return


def exec_command(args):
    """
    :param args: str or list
    :return: stdout
    """
    p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
    print('---- exec command: {0}'.format(args))
    (o, _) = p.communicate()
    stdout = o.decode('utf-8').strip()
    return stdout


def init_dirs():
    from common import need_init_dirs, presto_etc_dir, presto_etc_link
    mkdir_pattern = 'mkdir -p {0}'
    for d in need_init_dirs:
        exec_command(mkdir_pattern.format(d))
    exec_command('ln -s {0} {1}'.format(presto_etc_dir, presto_etc_link))
    return


def create_connectors():
    from common import presto_catalog_dir, connectors_to_add

    json_root = json.loads(connectors_to_add)
    for connector in json_root:
        connector_name = connector['catalog']
        connector_file = os.path.join(presto_catalog_dir, connector_name+'.properties')
        print('---- add connector_file: {0}'.format(connector_file))
        with open(connector_file, 'w') as f:
            for l in connector['config']:
                f.write('{0}\n'.format(l))
    return


def delete_connectors():
    from common import presto_catalog_dir, connectors_to_delete

    json_root = json.loads(connectors_to_delete)
    for connector_name in json_root:
        connector_file = os.path.join(presto_catalog_dir, connector_name+'.properties')
        print('---- remove connector_file: {0}'.format(connector_file))
        exec_command('rm -f {0}'.format(connector_file))
    return
