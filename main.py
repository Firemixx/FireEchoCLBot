import discord
from discord.ext import tasks
import os
import asyncio
from dotenv import load_dotenv
import time
import logging
from Logic import logging as log
from Logic.Parsing import ParsingSystem as pars
from Logic.DB import parsDB as db
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

logger=logging.getLogger(__name__)
load_dotenv('Storage/.env')
token = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    log.config_log(level=logging.INFO)
    logger.info(f"We have logged in as {bot.user}")
    await db.Init()
    parsPR.start()
    parsComm.start()


@tasks.loop(seconds=30)
async def parsPR():
    log.config_log(level=logging.INFO)
    logger.info("Parsing PR's")
    await pars.parsPR(bot)

@tasks.loop(minutes=40)
async def parsComm():
    log.config_log(level=logging.INFO)
    logger.info('Start parsing comments')
    await pars.parsComments(bot)

bot.run(token)