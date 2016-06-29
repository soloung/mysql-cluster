import json
import httplib
import clusterLog


def test():
    x = "s s s"
    x = x.replace(' ','')
    clusterLog.logger.info(x)
    return "sssssssssssssssssss"

a = test()
clusterLog.logger.info(a)


