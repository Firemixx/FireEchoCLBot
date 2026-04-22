import discord
from discord.ext import tasks
import os
import asyncio
from dotenv import load_dotenv
import time
import logging
import github
from Logic import logging as log
from Logic.Parsing import ParsingSystem as pars
from Logic.DB import parsDB as db
from Logic.DS import MessageMenager as msg
from Logic.Localization import LocalizationManager as loc
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
    await db.init_db()
    await loc.init()
    parsPR.start()
    parsComm.start()
    checkUpMerged.start()


@tasks.loop(seconds=30)
async def parsPR():
    log.config_log(level=logging.INFO)
    logger.info("Parsing PR's")
    try:
        await pars.parsPR(bot)
    except github.UnknownObjectException:
        logger.warning('PR is not created!')
    except Exception as e:
        logger.error(f'PR parsing have error:{e}')
        await msg.sendEmail()
        

@tasks.loop(minutes=40)
async def parsComm():
    log.config_log(level=logging.INFO)
    logger.info('Start parsing comments')
    try:
        await pars.parsComments(bot)
    except Exception as e:
        logger.error(f'PR parsing have error:{e}')
        await msg.sendEmail()

@tasks.loop(seconds=30)
async def checkUpMerged():
    log.config_log(level=logging.INFO)
    logger.info("Checking up merger pr's")
    try:
        await pars.checkUpMerged(bot)
    except Exception as e:
        logger.error(f'PR parsing have error:{e}')
        await msg.sendEmail()

bot.run(token)