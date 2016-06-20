#coding=utf-8
import subprocess
import time
import writeConfig
import sys
import os

###### create etcd cluster
subprocess.Popen(["etcd" ,"-proxy", "on","-listen-client-urls", "http://127.0.0.1:2379","-initial-cluster", "etcd0=http://etcd0:2380,etcd1=http://etcd1:2380,etcd2=http://etcd2:2380"])
time.sleep(5);
print("end");
#####

##### pull mysql config from etcd cluster
mysql_configs = subprocess.check_output("etcdctl get mysql-configs",shell=True);
mysql_configs = mysql_configs.strip('\n');
keyList = mysql_configs.split(',');
for key in keyList:
    #set data into my.cnf
    #here key should be changed -> clusterId + key
    value = subprocess.check_output(["etcdctl","get",key]);
    key_value = "the key is %s,value is %s" %(key,value)

    print key_value
    writeConfig.writeConfig2File(key,value,"/etc/mysql/my.cnf");
    #writeConfig.watchKeyValueChangeHandle(key)

###### start mysql
execMysqlCmd = "mysqld --init-file=/tmp/mysql-first-time.sql";
# 1) get the state from etcd to check if the cluster is create first time
clusterId = os.environ.get("WSREP_CLUSTER_ID");
key = clusterId + "-first-start";
clusterState = subprocess.check_output(["etcdctl","get",key]);
clusterState = clusterState.strip('\n');
nodeId = os.environ.get("WSREP_NODE_ID");

if clusterState == "true":
    mysqlProcess = subprocess.Popen(execMysqlCmd,shell=True);
    #subprocess.check_output(["etcdctl","set",key,"false"]);
    writeConfig.writeConfig2File(nodeId,"start mysql and write cluster statue false","/pod-log.log");
else:
    mysqlProcess = subprocess.Popen("exec mysqld --init-file=/tmp/second_start.sql",shell=True);
    writeConfig.writeConfig2File(nodeId,"start mysql","/pod-log.log");


###### here when pod was recreated,the mysql will be delete

#mysqlProcess = subprocess.Popen(execMysqlCmd,shell=True);
#TODO
#writeConfig.writeConfig2File("start mysql process",sys.argv[1],"/pod-log.log");
#print("start mysql ");



###### watch the key which when changed should restart mysql service

watch_configs = subprocess.check_output("etcdctl get watch-configs",shell=True);
watch_configs = watch_configs.strip('\n');
keyList = watch_configs.split(',')
for key in keyList:
    writeConfig.watchKeyValueChangeHandle(key)


#
while True:
    time.sleep(10000)
#####