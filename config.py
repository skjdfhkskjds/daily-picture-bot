import os
import json
import logging
from dotenv import load_dotenv

class Config:
    def __init__(self):
        logger = logging.getLogger(__name__)
        config = load_config()
        self.retry_attempts = config["RETRY_ATTEMPTS"]
        self.names_file = config["PROJECT_ROOT"]+config["NAMES_FILE"]
        self.discord = load_discord_config(logger, config)
        self.mega = load_mega_config(logger, config)
        self.log = load_log_config(logger, config)

    def get_retry_attempts(self):
        return self.retry_attempts
    
    def get_names_file(self):
        return self.names_file

    def get_discord(self):
        return self.discord

    def get_mega(self):
        return self.mega

    def get_log(self):
        return self.log

def load_config(path):
    with open(path, 'r') as f:
        config = json.load(f)
        return config

# Load the discord config
def load_discord_config(logger, config):
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    try:
        discord_config = config['DISCORD_CONFIG']
    except KeyError:
        logger.error("DISCORD_CONFIG not found in config.json")
        exit(1)

    discord_config["TOKEN"] = token
    discord_config["NAMES_FILE"] = config["PROJECT_ROOT"]+config["NAMES_FILE"]
    discord_config["ATTACHMENTS_PATH"] = config["PROJECT_ROOT"]+config["ATTACHMENTS_PATH"]
    return discord_config

# Load the mega config
def load_mega_config(logger, config):
    load_dotenv()
    # load mega username and password
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    try:
        mega_config = config['MEGA_CONFIG']
    except KeyError:
        logger.error("MEGA_CONFIG not found in config.json")
        exit(1)
    
    mega_config["USERNAME"] = username
    mega_config["PASSWORD"] = password
    mega_config["ATTACHMENTS_PATH"] = config["PROJECT_ROOT"]+config["ATTACHMENTS_PATH"]
    return mega_config

def load_log_config(logger, config):
    try:
        log_config = config['LOG_CONFIG']
    except KeyError:
        logger.error("LOG_CONFIG not found in config.json")
        exit(1)
    
    log_config["LOGFILE_PATH"] = config["PROJECT_ROOT"]+log_config["LOGFILE_PATH"]
    return log_config
