import os
import time
from discord.ext import tasks
import random
import discord
from mega import Mega
from dotenv import load_dotenv

ATTACHMENTS_PATH = 'attachments'
MAX_FILE_SIZE = 8 * 1024 * 1024

intents = discord.Intents.default()
client = discord.Client(intents=intents)

load_dotenv()

# load discord token
token = os.getenv('DISCORD_TOKEN')
channel = os.getenv('CHANNEL_ID')
channel_id = int(channel)

# load mega username and password
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

@client.event
async def on_ready():
    print("hehe haha we up frfr")

# returns the path to the image
def get_image():
    mega = Mega()
    m = mega.login(username, password)

    files = m.get_files()
    extracted = []
    for x in files:
        if files[x]['t'] == 0:
            extracted.append(files[x]['a']['n'])

    # .jpg, .png, .heic filter
    extracted = [file for file in extracted if file.endswith(('.jpg', '.png', '.heic'))]
    
    # while True:
    random_file_image = random.choice(extracted)
    file = m.find(random_file_image)
    print("file found", file)

    path = m.download(file, dest_path=ATTACHMENTS_PATH)
    print("file downloaded", path)

    if os.path.getsize(path) < MAX_FILE_SIZE:
        # break

        print(os.path.getsize(path)) 
    time.sleep(5)
    if path.name.endswith('.heic'):
        os.system(f"magick convert '{ATTACHMENTS_PATH}/{path.name}' '{ATTACHMENTS_PATH}/{path.name.replace('.heic', '.jpg')}'")
        return path.name.replace('.heic', '.jpg')

    return path.name

@tasks.loop(hours=24)
async def send_image():
    path = get_image()
    picture = discord.File(ATTACHMENTS_PATH+'/'+path)
    c = client.get_channel(channel_id)
    if c is None:
        print("Error: Channel not found. Make sure the channel ID is correct.")
        return
    
    await c.send(file=picture)
    cleanup()

@send_image.before_loop
async def before():
    await client.wait_until_ready()

def cleanup():
    os.system(f"rm -rf {ATTACHMENTS_PATH}/*")

async def setup_hook():
    send_image.start()

if __name__ == '__main__':
    client.setup_hook = setup_hook
    client.run(token)