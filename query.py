import os
import random
from mega import Mega
from config import *
from PIL import Image
import hashlib

# returns the path to the image
def get_image(config):
    path = getFromMega(config)
    if path.name.endswith('.heic'):
        return convertHEICToJPG(config[MAGICK_PATH], f'{config[ATTACHMENTS_PATH]}/{path.name}')

    return path.name

# Gets a random file from mega.nz
def getFromMega(config):
    mega = Mega()
    m = mega.login(config[USERNAME], config[PASSWORD])

    files = m.get_files()
    extracted = []
    for x in files:
        if files[x]['t'] == 0:
            extracted.append(files[x]['a']['n'])

    # extensions filter
    extracted = [file for file in extracted if file.endswith(tuple(ext for ext in config[FILE_TYPES]))]

    while True:
        random_file_image = random.choice(extracted)
        file = m.find(random_file_image)
        path = m.download(file, dest_path=config[ATTACHMENTS_PATH])
        if os.path.getsize(path) < config[MAX_FILE_SIZE]:
            break
    return path

# Convets HEIC to JPG and removes the old file
def convertHEICToJPG(magick, path):
    os.system(f"{magick} convert '{path}' '{path.replace('.heic', '.jpg')}'")
    os.system(f"rm '{path}'")
    return path.replace('.heic', '.jpg')

# Get unique hash from image
def get_image_hash(path):
    with Image.open(path) as img:
        # Ensure uniformity by scaling
        img = img.convert('RGB').resize((800, 600))
        img_bytes = img.tobytes()
        # Generate unique hash from bytes using sha-256
        img_hash = hashlib.sha256(img_bytes).hexdigest()
    return img_hash

