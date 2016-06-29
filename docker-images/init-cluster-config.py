#coding=utf-8
import subprocess
import time
import writeConfig
import sys
import os

clusterId = clusterId = os.environ.get("WSREP_CLUSTER_ID");
mysql_configs = writeConfig.getConfigFromEtcd("mysql-configs")
keyList = mysql_configs.split(',');
for key in keyList:
    value = getConfigFromEtcd(key);
    setConfig2Etcd(clusterId + key,value):


