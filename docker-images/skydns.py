#coding=utf-8
import json
import httplib
import clusterLog

def putValue2SkyDNS(skyDNSIp,skyDNSPort,clusterId,nodeId,value):
    # print "input value : " + value 
    logger.info(" will set the value %s to skydns clusterId is %s,nodeId is %s",value,clusterId,nodeId)
    conn = httplib.HTTPConnection(skyDNSIp,skyDNSPort)
    conn.request("PUT","/v2/keys/skydns/local/cluster/mysql-"+clusterId + "/" + nodeId+ "?" + "value=" + value ,value)
    res = conn.getresponse()
    conn.close()
    if res.status == 200 :
        logger.info("set skydns ok")
    else:
        logger.error("can't set the value :%s to SkyDNS",value)
        logger.error("skyDns ip %s:%d%s",skyDNSIp,skyDNSPort,"/v2/keys/skydns/local/cluster/mysql-"+clusterId  + "/" + nodeId+ "?" + "value=" + value)
        logger.error("http res code:%d,res reason %s",res.status,res.reason)
    return 0

def getValueFromSkyDNS(skyDNSIp,skyDNSPort,clusterId):
    conn = httplib.HTTPConnection(skyDNSIp,skyDNSPort)
    conn.request("GET","/v2/keys/skydns/local/cluster/mysql-"+clusterId )

    res = conn.getresponse()
    data = res.read()
    print "-----------get value from sky DNS"
    print res.status
    print data
    conn.close()
    if res.status == 200 :
        jsonObj = json.loads(data)
        valueStr = jsonObj["node"]["nodes"][0]["value"]
    else:
        logger.error("can't get the value : %s", clusterId)

def getPodHostIP(kuberIp,kuberPort,namespace,podname):
    conn = httplib.HTTPConnection(kuberIp,kuberPort)
    conn.request("GET","/api/v1/namespaces/"+namespace + "/pods/" + podname)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    hostIp=""
    print data
    print "-----------------------"
    if res.status == 200 :
        jsonObj = json.loads(data)
        hostIp = jsonObj["status"]["hostIP"]
        print "ip:" + jsonObj["status"]["hostIP"]
        logger.info("host ip : %s",hostIp)
    else:
        logger.error("can't find the pod:%s in namespace %s",podname, namespace)
    return hostIp

def getServicePort(kuberIp,kuberPort,namespace,serviceName):
    conn = httplib.HTTPConnection(kuberIp,kuberPort)
    conn.request("GET","/api/v1/namespaces/"+namespace + "/services/" + serviceName)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    hostPort = 0;
    print data
    print "----------getServicePort-------------"
    if res.status == 200 :
        jsonObj = json.loads(data)
        port0 = jsonObj["spec"]["ports"][0]
        print port0["nodePort"]
        hostPort = port0["nodePort"]
        logger.info("service port is %d",hostPort)
    else:
        logger.error("can't find the service:%s in namespace %s",serviceName, namespace)
    return hostPort

#################################################################
logger = clusterLog.getLogger()

if __name__ == '__main__':
    logger.info("-------------------------------------------------")
    getPodHostIP("192.168.48.103",8080,"default","mysql-node2tll7by61-dkcm0")
    getServicePort("192.168.48.103",8080,"default","mysql-clusterxx")
    hostObj = {}
    hostObj["host"] = "192.168.48.99"
    hostObj["port"] = 31002
    hostObjStr = json.dumps(hostObj)
    hostObjStr = hostObjStr.replace(' ','')

    putValue2SkyDNS("192.168.48.103",2379,"yy","1",hostObjStr)
    getValueFromSkyDNS("192.168.48.103",2379,"yy")