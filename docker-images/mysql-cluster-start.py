#coding=utf-8
import subprocess
import time
import writeConfig
import sys
import os
import initCluster
import skydns
import clusterLog
import json



def proxyEtcd():
    subprocess.Popen(["etcd" ,"-proxy", "on","-listen-client-urls", "http://127.0.0.1:2379","-initial-cluster", "etcd0=http://etcd0:2380,etcd1=http://etcd1:2380,etcd2=http://etcd2:2380"])
    time.sleep(5);
    logger.info("proxy etcd start")

def startWatchKey():
    clusterId = os.environ.get("WSREP_CLUSTER_ID");
    watch_configs = writeConfig.getConfigFromEtcd("watch-configs")
    keyList = watch_configs.split(',')
    for key in keyList:
        writeConfig.watchKeyValueChangeHandle(clusterId,key)
    logger.info("start watch key")

def checkClusterFirstTimeStart():
    clusterId = os.environ.get("WSREP_CLUSTER_ID");
    key = clusterId + "-first-start";
    clusterFirstTimeStart = writeConfig.getConfigFromEtcd(key);
    if clusterFirstTimeStart == "true":
        initCluster.initClusterConfig2Etcd(clusterId)
    return clusterFirstTimeStart

def writeConfig2LocalFromEtcd():
    clusterId = os.environ.get("WSREP_CLUSTER_ID");
    mysql_configs = writeConfig.getConfigFromEtcd("mysql-configs")
    keyList = mysql_configs.split(',');
    for key in keyList:
        value = subprocess.check_output(["etcdctl","get",clusterId + key]);
        writeConfig.writeConfig2File(key,value,"/etc/mysql/my.cnf");

def mysqlStartInitWithSqlFile(isCLusterFirstTimeStart):
    clusterId = os.environ.get("WSREP_CLUSTER_ID");
    key = clusterId + "-first-start";
    if isCLusterFirstTimeStart == "true":
        execMysqlCmd = "exec mysqld --init-file=/tmp/mysql-first-time.sql";
        mysqlProcess = subprocess.Popen(execMysqlCmd,shell=True);
        writeConfig.setConfig2Etcd(key,"false");
        logger.info("start mysql with mysql-first-time.sql")
    else:
        mysqlProcess = subprocess.Popen("exec mysqld --init-file=/tmp/second_start.sql",shell=True);
        logger.info("start mysql with second_start.sql")

def setHostIp2SkyDns():
    hostname = os.environ.get("HOSTNAME")
    clusterId = os.environ.get("WSREP_CLUSTER_ID");
    hostip = skydns.getPodHostIP("192.168.48.103",8080,"default",hostname)
    serviceName = clusterId
    hostport = skydns.getServicePort("192.168.48.103",8080,"default",serviceName)
    nodeId = os.environ.get("WSREP_NODE_ID")
    
    hostObj = {}
    hostObj["host"] = hostip
    hostObj["port"] = hostport

    hostStr = json.dumps(hostObj)
    hostStr = hostStr.replace(' ','')

    skydns.putValue2SkyDNS("192.168.48.103",2379,clusterId,nodeId,hostStr)

def start_mysql():
    proxyEtcd()
    clusterFirstTimeStart = checkClusterFirstTimeStart()
    writeConfig2LocalFromEtcd()
    mysqlStartInitWithSqlFile(clusterFirstTimeStart)
    startWatchKey()
    setHostIp2SkyDns()

#####
if __name__ == "__main__":
    logger = clusterLog.getLogger()
    start_mysql()
    while True:
        time.sleep(10000)
#####