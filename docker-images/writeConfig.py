#coding=utf-8
import os
import subprocess
import sys
import clusterLog


def fileHandle(str):
    return
#watch the key-value with restart mysql
def watchKeyValueChangeHandle(clusterId,key):
    print "watch key value change handle"
    process = subprocess.Popen(["etcdctl","exec-watch",clusterId + key,"--","python","restart-mysql.py",key]);
    return

#write the config into my.cnf
def writeConfig2File(key,value,fileName):
    fopen = open(fileName,'r');
    w_str = "";
    hasKeyFlag = False;
    for line in fopen.readlines():
        if line.find(key) != -1 :
            line = key + "=" + value + "\n"
            hasKeyFlag = True;
            w_str += line
        else:
            w_str += line

    if hasKeyFlag == False :
        w_str += key + "=" + value + "\n"

    fopen.close();
    fwrite = open(fileName,'w');
    fwrite.write(w_str);
    fwrite.close();
    return

def writeConfigs2File(keyValueMap):
    return;

def getConfigFromEtcd(key):
    getFlag = False;
    getTimes = 0;
    value="";
    while getFlag == False and getTimes<20:
        try:
            getTimes = getTimes + 1;
            value = subprocess.check_output("etcdctl get "+key,shell=True);
        except Exception, e:
            clusterLog.logger.info("getConfig %s frm etcd error ",key)
        else:
            getFlag = True;
        finally:
            pass
    value = value.strip('\n');
    return value;

def setConfig2Etcd(key,value):
    setFlag = False
    setTimes = 0
    while setFlag == False and setTimes < 20:
        try:
            setTimes = setTimes + 1;
            subprocess.check_output(["etcdctl","set",key,value]);
        except Exception, e:
            clusterLog.logger.info("setConfig  %s error when set key",key)
        else:
            setFlag = True;
        finally:
            pass
    return;