import logging

logger = logging.getLogger(__name__)

fileHandler = logging.FileHandler("logfile.log")

logger.addHandler(fileHandler)  #filahandler object


logger.debug("A debug statement is executed")
logger.info("Information statement")
logger.warning("Something is in warning mode")
logger.error("A Major error has happened")
logger.critical("Critical issue")