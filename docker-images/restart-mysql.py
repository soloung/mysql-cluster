import subprocess
import sys
import writeConfig
import os
import time

print sys.argv[1] 

#func restart mysql service
#Note: the restart order
def restartMysqlService(key):
    key = sys.argv[1];
    value = subprocess.check_output(["etcdctl","get",key]);
    value = value.strip('\n');
    writeConfig.writeConfig2File(key,value,"/etc/mysql/my.cnf");

    #pid = subprocess.check_output("pgrep mysql",shell=True);
    #pid = pid.strip('\n');
    #killResult = subprocess.check_output(["kill","-9",pid]);# here a Zombie process will be created
    restartResult = subprocess.check_output(["service","mysql","stop"]);
    #start mysql
    ##execCmd = "exec mysqld --init-file=/tmp/mysql-first-time.sql";
    nodeId = os.environ.get("WSREP_NODE_ID");
    int_nodeId = int(nodeId);
    time.sleep((i+1)*5); # all node should be shut down,and then first,second ,,,start
    process = subprocess.Popen(["service","mysql","start"]);

#restart
restartMysqlService(sys.argv[1]);
