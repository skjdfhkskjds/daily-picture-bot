import os
import random
from mega import Mega

# returns the path to the image
def get_image(config):
    path = getFromMega(config)
    if path.name.endswith('.heic'):
        return convertHEICToJPG(f'{config["ATTACHMENTS_PATH"]}/{path.name}')

    return path.name

# Gets a random file from mega.nz
def getFromMega(config):
    mega = Mega()
    m = mega.login(config["USERNAME"], config["PASSWORD"])

    files = m.get_files()
    extracted = []
    for x in files:
        if files[x]['t'] == 0:
            extracted.append(files[x]['a']['n'])

    # extensions filter
    extracted = [file for file in extracted if file.endswith(tuple(ext for ext in config["FILE_TYPES"]))]
    
    while True:
        random_file_image = random.choice(extracted)
        file = m.find(random_file_image)
        path = m.download(file, dest_path=config["ATTACHMENTS_PATH"])
        if os.path.getsize(path) < config["MAX_FILE_SIZE"]:
            break
    return path

# Convets HEIC to JPG and removes the old file
def convertHEICToJPG(path):
    os.system(f"/home/ec2-user/imagemagick/bin/magick convert '{path}' '{path.replace('.heic', '.jpg')}'")
    os.system(f"rm '{path}'")
    return path.replace('.heic', '.jpg')
