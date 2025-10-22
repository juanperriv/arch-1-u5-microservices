import logging

LOGGER: logging.Logger = logging.getLogger(__name__)

def log_info(msg: str):
    LOGGER.info("[SALES] " + msg)