import os
import discord
from log import NewLogger

async def ping_role(ctx, role_name):
    # Find the role in the guild by its name
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    await ctx.send(role.mention)

async def send_image(logger, file, client, config):
    picture = discord.File(get_file(config["ATTACHMENTS_PATH"]))
    c = client.get_channel(config["CHANNEL_ID"])
    if c is None:
        logger.error("Channel not found. Make sure the channel ID is correct.")
        return
    
    await c.send(file=picture)
    await ping_role(c, config["DISCORD_ROLE"])

def setup_event_handlers(logger, file, client, config):
    @client.event
    async def on_ready():
        logger.info('Bot is ready. Sending picture...')
        await send_image(logger, file, client, config)
    @client.event
    async def on_error(event_method, *args, **kwargs):
        logger.error(f'An error occurred in {event_method}: {args} {kwargs}')

def run_client(logger, file, config):
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    setup_event_handlers(logger, file, client, config)
    client.run(config["TOKEN"])
