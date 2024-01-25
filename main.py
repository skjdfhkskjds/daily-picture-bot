import os
import sys
from log import NewLogger
from config import Config
from query import get_image
from client import run_client

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print("Error: No arguments provided. Please provide an argument.")
        exit(1)

    config = Config()

    logger = NewLogger(config.get_log())
    if args[0] == "GET":
        logger.info("Fetching image...")
        logger.info(f'image at: {get_image(config.get_mega())}')
    elif args[0] == "POST":
        logger.info("Posting image...")
        attempts = 0
        while attempts < config.get_retry_attempts():
            discord_config = config.get_discord()
            attachments_files = os.listdir(discord_config['ATTACHMENTS_PATH'])
            if len(attachments_files) != 0:
                run_client(discord_config)
                logger.info("Cleaning up...")
                cleanup(config)
                break
            logger.error("No files found in attachments folder. Getting new image...")
            logger.info(f'image at: {get_image(config.get_mega())}')

def cleanup(config):
    os.system(f"rm -rf {config.get_mega()['ATTACHMENTS_PATH']}/*")
    os.system(f"rm -rf {config.get_log()['LOGFILE_PATH']}")

if __name__ == '__main__':
    main()