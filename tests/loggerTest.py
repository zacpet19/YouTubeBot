import sys
sys.path.append('..')

from Logger import Logger

def loggerTest():
    logger = Logger()
    assert type(logger) == Logger
    logger.warn("this is a warning")
    logger.debug("this is a debug")
    logger.info("this is a info")
    logger.error("this is an error")
    assert logger.name == "Epic logger"

loggerTest()
