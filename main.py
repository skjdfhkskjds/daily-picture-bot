import os
import sys
from log import NewLogger
from config import Config
from query import get_image
from client import run_client
from ai.detect_users import get_face_data
from ai.annotate import annotate_image

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
                run_client(logger, get_file(discord_config['ATTACHMENTS_PATH']), discord_config)
                logger.info("Cleaning up...")
                cleanup(config)
                break
            logger.error("No files found in attachments folder. Getting new image...")
            logger.info(f'image at: {get_image(config.get_mega())}')
    elif args[0] == 'ANNOTATE':
        logger.info("Detecing users in image...")
        file = get_file(config.get_discord()['ATTACHMENTS_PATH'])
        face_data = get_face_data(file, file.split('/')[-1])
        logger.info("Users detected.")
        logger.info("Annotating image...")
        annotate_image(file, face_data)

def get_file(attachments_path):
   files = os.listdir(attachments_path)
   return f'{attachments_path}/{files[0]}'

def cleanup(config):
    os.system(f"rm -rf {config.get_mega()['ATTACHMENTS_PATH']}/*")
    os.system(f"rm -rf {config.get_log()['LOGFILE_PATH']}")

if __name__ == '__main__':
    main()