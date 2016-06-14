#coding=utf-8
import os
import subprocess
import sys
def fileHandle(str):
    return

def watchKeyValueChangeHandle(key):
    print "watch key value change handle"
    process = subprocess.Popen(["etcdctl","exec-watch",key,"--","python","restart-mysql.py",key]);
    return

#配置写入文件
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

#writeConfig2File("key1","value1","a.txt");