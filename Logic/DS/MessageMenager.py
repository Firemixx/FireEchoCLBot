import discord
import asyncio
import os
import logging
from Logic import logging as log
from Logic.DB import parsDB as db
from Logic.Localization import LocalizationManager as loc
from pathlib import Path
from dotenv import load_dotenv, set_key
import smtplib
from email.message import EmailMessage

logger=logging.getLogger(__name__)
env_path = Path(__file__).resolve().parents[2] / "Storage" / ".env"
logs_path = Path(__file__).resolve().parents[2] / "Storage" / "logs.txt"

async def createEmded(name:str, author:str, status:str, aboute:str, why:str, changelog:str,URL:str, bot: discord.Client)->int:
    log.config_log(level=logging.INFO)
    embed= discord.Embed(title=f"{await loc.get_loc("created_pr")} 🔨{name} || ({status})", description=f"{await loc.get_loc("author_pr")} {author}\n\n {await loc.get_loc("aboute_pr")} {aboute}\n\n {await loc.get_loc("why_pr")}{why}\n\n{await loc.get_loc("changelog_pr")} \n {changelog}", color=0x008200, url=URL)
    load_dotenv(env_path)
    channel_id=os.getenv("CHANNEL_DEV_ID")
    guild_id=os.getenv("GUILD_ID")
    if (channel_id!='' and guild_id!=''):
        logger.info(".env channel id is not null")
        integer_chanId=int(channel_id)
        g= bot.get_guild(int(guild_id))
        channelIfInteger=g.get_channel(integer_chanId)
        await channelIfInteger.send(embed=embed)
        logger.info("PR sended")
        async for message in channelIfInteger.history(limit=1):
            if (message.author==bot.user):
                thread = await message.create_thread(
                name=f"{await loc.get_loc("thread_pr_dev_name")}",
                auto_archive_duration=60
                )
                await thread.send(f"{os.getenv("BOT_NAME")} {await loc.get_loc("thread_pr_dev_text")}")
                logger.info('Thread created')
                return thread.id
                
async def sendToBranch(author:str,commentContent:str,idThread:int,time ,bot: discord.Client):
    log.config_log(level=logging.INFO)
    embed= discord.Embed(title=f"{await loc.get_loc("message_pr_name")} {author}", description=f"{await loc.get_loc("message_pr_content")} \n{commentContent}\nВ: ⌚{time}", color=0xffff00)
    load_dotenv(env_path)
    channel_id=os.getenv("CHANNEL_DEV_ID")
    guild_id=os.getenv("GUILD_ID")
    if (channel_id!=''):
        logger.info(".env channel id is not null on comment publishing")
        integer_chanId=int(channel_id)
        g= bot.get_guild(int(guild_id))
        channelIfInteger=g.get_channel(integer_chanId)
        thread=channelIfInteger.get_thread(idThread)
        if (len(commentContent)>4000):
            await thread.send(f"{await loc.get_loc("limit_simbols_text",author)}{commentContent}")
            logger.info("comment sended like text")
        else:
            await thread.send(embed=embed)
            logger.info("comment sended like embed")


async def sendToPublicChangelog(changelog:str,title:str, bot: discord.Client):
    log.config_log(level=logging.INFO)
    embed= discord.Embed(title=f"{await loc.get_loc("public_CL_name")} \n {changelog}", color=0x008200)
    load_dotenv(env_path)
    channel_id=os.getenv("CHANNEL_CL_ID")
    guild_id=os.getenv("GUILD_ID")
    if (channel_id!='' and guild_id!=''):
        logger.info(".env channel id is not null")
        integer_chanId=int(channel_id)
        g= bot.get_guild(int(guild_id))
        channelIfInteger=g.get_channel(integer_chanId)
        await channelIfInteger.send(embed=embed)
        logger.info("PR sended")
        async for message in channelIfInteger.history(limit=1):
            if (message.author==bot.user):
                thread = await message.create_thread(
                name=f"{await loc.get_loc("thread_pr_public_name")}",
                auto_archive_duration=60
                )
                if(os.getenv("PUBLIC_CL_DS_ROLE")==''):
                    await thread.send(f"{os.getenv("BOT_NAME")} {await loc.get_loc("thread_pr_public_text_withoute_role")}")
                else:
                    await thread.send(f"{await loc.get_loc("thread_pr_public_text",title)}"+f"<@&{int(os.getenv("PUBLIC_CL_DS_ROLE"))}>")
                logger.info('Thread created')

async def sendEmail():
    load_dotenv(env_path)
    with open(logs_path) as file:
        msg=EmailMessage()
        msg.set_content(file.read())
    msg['Subject'] = os.getenv("EMAIL_SUBJECT")
    msg['From'] = os.getenv("EMAIL_OF_BOT")
    msg['To'] = os.getenv("EMAIL_OF_RECIEVER")
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login(
            os.getenv("EMAIL_OF_BOT"),
            os.getenv("EMAIL_PASSWORD")
        )
        s.send_message(msg)
    with open(logs_path, 'w') as file:
        pass