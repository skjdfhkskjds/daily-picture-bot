import logging
from colorlog import ColoredFormatter

def NewLogger(config):
    log_level = get_log_level(config["LOG_LEVEL"])

    formatter = ColoredFormatter(config["LOG_FORMAT"], datefmt=None, reset=True, log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }, secondary_log_colors={}, style='%')

    file_handler = logging.FileHandler(config["LOGFILE_PATH"])
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def get_log_level(log_level):
    if log_level == "DEBUG":
        return logging.DEBUG
    elif log_level == "INFO":
        return logging.INFO
    elif log_level == "WARNING":
        return logging.WARNING
    elif log_level == "ERROR":
        return logging.ERROR
    return logging.CRITICAL