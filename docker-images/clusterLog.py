#coding=utf-8
import logging
import logging.config


def logInit():
    logging.config.fileConfig('./logging.conf')

def getRootLogger():
    logger = logging.getLogger("root")
    return logger
def getLogger():
    logger = logging.getLogger("root")
    return logger

def test_log():
    logger.info("message id : %d str: %s",1,"xxxx")

logInit()
logger = getLogger()
if __name__ == '__main__':
    test_log()