import subprocess
import time
import writeConfig
import sys

###### create etcd cluster
subprocess.Popen(["etcd" ,"-proxy", "on","-listen-client-urls", "http://127.0.0.1:2379","-initial-cluster", "etcd0=http://etcd0:2380,etcd1=http://etcd1:2380,etcd2=http://etcd2:2380"])
time.sleep(5);
print("end");
#####

##### pull mysql config from etcd cluster
mysql_configs = subprocess.check_output("etcdctl get mysql-configs",shell=True);
mysql_configs = mysql_configs.strip('\n');
keyList = mysql_configs.split(',');
print(mysql_configs);
num = len(keyList);
print(num)
for key in keyList:
    #set data into my.cnf
    value = subprocess.check_output(["etcdctl","get",key]);
    key_value = "the key is %s,value is %s" %(key,value)

    print key_value
    writeConfig.writeConfig2File(key,value,"/etc/mysql/my.cnf");
    #writeConfig.watchKeyValueChangeHandle(key)

###### start mysql
mysqlProcess = subprocess.Popen(sys.argv[1],shell=True);
print("start mysql ");

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