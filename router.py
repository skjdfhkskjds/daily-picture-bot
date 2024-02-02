import os
from query import get_image
from client import run_client
from ai.annotate import annotate_image
from ai.detect_users import get_face_data

# Handler for the 'GET' command
def get(logger, config):
    logger.info("Fetching image...")
    logger.info(f'image at: {get_image(config.get_mega())}')

# Handler for the 'POST' command
def post(logger, config):
    discord_config = config.get_discord()
    logger.info("Posting image...")
    attempts = 0
    while attempts < config.get_retry_attempts():
        file_path = get_file(discord_config['ATTACHMENTS_PATH'])
        if file_path:
            run_client(logger, file_path, discord_config)
            cleanup(logger, config)
            break
        logger.error("No files found in attachments folder. Getting new image...")
        get(logger, config)
        attempts += 1

# Handler for the 'ANNOTATE' command
def annotate(logger, config):
    file_path = get_file(config.get_mega()['ATTACHMENTS_PATH'])
    if not file_path:
        logger.error("No files found in attachments folder.")
        return
    logger.info("Detecing users in image...")
    face_data, names = get_face_data(config.get_names_file(), file_path, file_path.split('/')[-1])
    logger.info(f"Users detected: {names}")

    logger.info("Annotating image...")
    annotated_image = annotate_image(file_path, face_data)
    logger.info(f'Annotated image at: {annotated_image}')

# Handler for the 'CLEANUP' command
def cleanup(logger, config):
    logger.info("Cleaning up...")
    os.system(f"rm -rf {config.get_mega()['ATTACHMENTS_PATH']}/*")
    os.system(f"rm -rf {config.get_log()['LOGFILE_PATH']}")

# get_file returns the first file in the attachments folder
# or None if there are no files
def get_file(attachments_path):
   files = os.listdir(attachments_path)
   if len(files) == 0:
       return None
   return f'{attachments_path}/{files[0]}'

# Register for all commands
commands = {
    "GET": get,
    "POST": post,
    "ANNOTATE": annotate,
    "CLEANUP": cleanup,
}
