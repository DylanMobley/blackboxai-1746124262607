import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    os.makedirs("logs", exist_ok=True)

    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
    )
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(stream)

    return logger
