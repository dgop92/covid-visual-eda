import logging
from config.logging import config_logger

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    config_logger()
    logger.info("app started")