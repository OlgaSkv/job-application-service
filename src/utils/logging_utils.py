import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(config=None):
    """Set up logging based on the configuration dict."""
    log_file = (
        config.get("logging", {}).get("file", "./logs/job_tracker.log")
        if config
        else "./logs/job_tracker.log"
    )
    log_level = config.get("logging", {}).get("level", "INFO").upper() if config else "INFO"
    max_log_size = (
        config.get("logging", {}).get("max_size", 5 * 1024 * 1024) if config else 5 * 1024 * 1024
    )
    backup_count = config.get("logging", {}).get("backup_count", 3) if config else 3

    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_log_size, backupCount=backup_count, encoding="utf-8"
    )
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.handlers.clear()  # Remove any existing handlers
    logger.addHandler(file_handler)

    # Console handler with UTF-8 encoding for Windows compatibility
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Suppress verbose logs from third-party libraries
    logging.getLogger("openai").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)
    logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.ERROR)

    logging.info("Job Tracker logging system initialized.")
