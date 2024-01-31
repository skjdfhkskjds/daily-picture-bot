import os
import discord
from log import NewLogger
from ai.detect_users import get_face_data
from ai.annotate import annotate_image

users = {
    "andie": 605209355318591509,
    "anette": 397959999751716865,
    "angela": 311599279405924353,
    "chauvin": 260421400714674176,
    "christie": 433254279784955905,
    "cindy": 649629755750088704,
    "colin": 408840905932406785,
    "daniel": 211996890902822914,
    "dominic": 260118797757841409,
    "dominy": 396522533458804748,
    "jaidyn": 488201280439844865,
    "justin": 368912019686031363,
    "marco": 81933717873893376,
    "michael": 271748826014941196,
    "michelle": 440608555318378497,
    "nolan": 646381481609920522,
    "ocean": 319618325217017856,
    "rachel": 688471323235582007,
    "rodmehr": 245629863006830593,
    "shirothie": 425451097662947329,
    "simon": 243123623278280706,
    "tam_an": 508022450617974815,
    "tee": 319628669318594580,
    "wendy": 148260985772310528,
}

async def ping_role(ctx, role_name):
    # Find the role in the guild by its name
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    await ctx.send(role.mention)

async def ping_users(ctx, names):
    msg = ""
    for name in names:
        if name not in users:
            continue
        user_id = users[name]
        msg += f'<@{user_id}>'
    await ctx.send(msg)

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
    await client.close()

def get_file(attachments_path):
   files = os.listdir(attachments_path)
   return f'{attachments_path}/{files[0]}'

async def send_annotated_image(logger, file_path, msg):
    logger.info("Detecing users in image...")
    face_data, names = get_face_data(file_path, file_path.split('/')[-1])
    logger.info("Users detected.")
    logger.info("Annotating image...")
    annotate_image(file_path, face_data)
    logger.info("Image annotated")

    thread = await msg.create_thread(
        name="Daily Picture Discussion"
    )
    logger.info("Thread created.")

    new_path = '_annotated.'.join(file_path.rsplit(".", 1))
    await thread.send(file=discord.File(new_path))
    await ping_users(thread, names)

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
