from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYY-MM-DD HH:mm:ss} | {level} | {message}",
)