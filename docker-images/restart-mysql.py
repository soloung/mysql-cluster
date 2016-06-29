import subprocess
import sys
import writeConfig
import os
import time
import clusterLog

print sys.argv[1] 

#func restart mysql service
#Note: the restart order
def restartMysqlService(key):
    clusterId = os.environ.get("WSREP_CLUSTER_ID");
    key = sys.argv[1];
    value = subprocess.check_output(["etcdctl","get",clusterId + key]);
    value = value.strip('\n');
    writeConfig.writeConfig2File(key,value,"/etc/mysql/my.cnf");


    restartResult = subprocess.check_output(["service","mysql","stop"]);
    nodeId = os.environ.get("WSREP_NODE_ID");
    logger.info("nodeId : %d mysql service stop",nodeId)
    int_nodeId = int(nodeId);
    time.sleep((i+1)*5); # all node should be shut down,and then first,second ,,,start
    process = subprocess.Popen(["service","mysql","start"]);
    logger.info("nodeId : %d mysql service start",nodeId)

#restart
if __name__ == '__main__':
    logger = clusterLog.getLogger()
    restartMysqlService(sys.argv[1]);
