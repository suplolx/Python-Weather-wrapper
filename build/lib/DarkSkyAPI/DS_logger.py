import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[*] %(levelname)s - %(asctime)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)