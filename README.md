# ambari-server-presto
Ambari custom server for [Presto](https://prestosql.io/)

# Support Presto Tarball Installation
Tested on
* Starburst Distribution of Presto version 302-e.9


# Installation
For `ambari-2.7.x`, `HDP-3.1`, `ambari-server-presto-0.1.2.tar.gz`
```
wget https://github.com/archongum/ambari-server-presto/releases/download/0.1.2/ambari-server-presto-0.1.2.tar.gz

sudo mkdir /var/lib/ambari-server/resources/stacks/HDP/3.1/services/PRESTO/

sudo tar -xvf ambari-server-presto-0.1.2.tar.gz -C /var/lib/ambari-server/resources/stacks/HDP/3.1/services/PRESTO/

# please setup 'package/config.ini'

# restart ambari
sudo ambari-server restart
```
