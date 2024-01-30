import os
import discord
from log import NewLogger
from ai.detect_users import get_face_data
from ai.annotate import annotate_image

async def ping_role(ctx, role_name):
    # Find the role in the guild by its name
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    await ctx.send(role.mention)

async def send_image(logger, client, config):
    file_path = get_file(config["ATTACHMENTS_PATH"])
    picture = discord.File(file_path)
    c = client.get_channel(config["CHANNEL_ID"])
    if c is None:
        logger.error("Channel not found. Make sure the channel ID is correct.")
        return
    
    message = await c.send(file=picture)
    await ping_role(c, config["DISCORD_ROLE"])
    await send_annotated_image(logger, file_path, message)

def get_file(attachments_path):
   files = os.listdir(attachments_path)
   return f'{attachments_path}/{files[0]}'

async def send_annotated_image(logger, file_path, msg):
    logger.info("Detecing users in image...")
    face_data = get_face_data(file_path, file_path.split('/')[-1])
    logger.info("Users detected.")
    logger.info("Annotating image...")
    annotate_image(file_path, face_data)

    thread = await msg.create_thread(
        name="Daily Picture Discussion",
        type=msg.public_thread
    )

    new_path = '_annotated.'.join(file_path.rsplit(".", 1))
    await thread.send(file=discord.File(new_path))

def setup_event_handlers(logger, client, config):
    @client.event
    async def on_ready():
        logger.info('Bot is ready. Sending picture...')
        await send_image(logger, client, config)
    @client.event
    async def on_error(event_method, *args, **kwargs):
        logger.error(f'An error occurred in {event_method}: {args} {kwargs}')

def run_client(logger, config):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    setup_event_handlers(logger, client, config)
    client.run(config["TOKEN"])
