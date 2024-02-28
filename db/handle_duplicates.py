from PIL import Image
import hashlib
from db import ImgGateway


# Get unique hash from image
def get_image_hash(path):
    with Image.open(path) as img:
        # Ensure uniformity by scaling
        img = img.convert('RGB').resize((800, 600))
        img_bytes = img.tobytes()
        # Generate unique hash from bytes using sha-256
        img_hash = hashlib.sha256(img_bytes).hexdigest()
    return img_hash


# TRUE if image exists in db
def is_duplicate(path, logger, config) -> bool:
    img_exists = False
    img_hash = get_image_hash(path)
    gw = ImgGateway(config.get_db_path())
    gw.create_connection()
    if gw.is_connected():
        logger.info(f"Connected to database")
        img_exists = gw.check_hash_exists(img_hash)
    else:
        logger.error(f"Could not establish db connection")
    gw.close_connection()
    return img_exists


# Inserts image <path> into db
def insert_img(path, logger, config) -> bool:
    inserted = False
    img_hash = get_image_hash(path)
    gw = ImgGateway(config.get_db_path())
    gw.create_connection()
    if gw.is_connected():
        logger.info(f"Connected to database")
        inserted = gw.insert_hash(img_hash)
        if inserted:
            logger.info(f"Inserted img into db")
        else:
            logger.error(f"Could not insert img into db")
    else:
        logger.error(f"Could not establish db connection")
    return inserted
