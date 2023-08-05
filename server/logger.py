import logging
import os


def setup_logging():
    """Set up logging handlers and format for application."""

    log_level = os.getenv("LOG_LEVEL", "DEBUG")
    default_format = "[%(asctime)s] %(levelname)s - %(module)s: %(message)s"
    logging.basicConfig(level=log_level, format=default_format)

    log_file = "/var/log/server.log"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(default_format))
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()
