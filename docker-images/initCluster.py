#coding=utf-8
import subprocess
import time
import writeConfig
import sys
import os

def initClusterConfig2Etcd(clusterId):
    mysql_configs = writeConfig.getConfigFromEtcd("mysql-configs")
    keyList = mysql_configs.split(',');
    for key in keyList:
        value = writeConfig.getConfigFromEtcd(key);
        writeConfig.setConfig2Etcd(clusterId + key,value)
