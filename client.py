import discord
from config import *

async def ping_role(ctx, role_name):
    # Find the role in the guild by its name
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    await ctx.send(role.mention)

async def ping_users(logger, config, ctx, names):
    msg = ""
    for name in names:
        if name not in config[USERNAMES]:
            continue
        user_id = config[USERNAMES][name]
        msg += f'<@{user_id}>'
    logger.info(f"Users pinged: {msg}")
    await ctx.send(msg)

async def send_image(logger, file_path, client, config):
    picture = discord.File(file_path)
    c = client.get_channel(config[CHANNEL_ID])
    if c is None:
        logger.error("Channel not found. Make sure the channel ID is correct.")
        return
    message = await c.send(file=picture)
    await ping_role(c, config[DISCORD_ROLE])
    
    logger.info(f"names file at:{config['NAMES_FILE']}")
    await send_annotated_image(logger, config, file_path, message)

async def send_annotated_image(logger, config, image_path, msg):
    # read the names from the name file
    logger.info("Reading names from file...")
    with open(config[NAMES_FILE], 'r') as file:
        names = file.readlines()
    names = [name.strip() for name in names]
    logger.info(f"names: {names}")

    logger.info("Creating thread...")
    thread = await msg.create_thread(
        name="Daily Picture Discussion"
    )
    logger.info("Thread created.")

    logger.info("Sending annotated image...")
    new_path = '_annotated.'.join(image_path.rsplit(".", 1))
    await thread.send(file=discord.File(new_path))
    logger.info("Pinging users...")
    await ping_users(logger, config, thread, names)

def setup_event_handlers(logger, file_path, client, config):
    @client.event
    async def on_ready():
        logger.info('Bot is ready. Sending picture...')
        await send_image(logger, file_path, client, config)
        await client.close()
    @client.event
    async def on_error(event_method, *args, **kwargs):
        logger.error(f'An error occurred in {event_method}: {args} {kwargs}')

def run_client(logger, file_path, config):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    setup_event_handlers(logger, file_path, client, config)
    client.run(config[DISCORD_TOKEN])
