import discord
import asyncio
import os
import logging
from Logic import logging as log
from Logic.DB import parsDB as db
from pathlib import Path
from dotenv import load_dotenv, set_key
import smtplib
from email.message import EmailMessage

logger=logging.getLogger(__name__)
env_path = Path(__file__).resolve().parents[2] / "Storage" / ".env"
logs_path = Path(__file__).resolve().parents[2] / "Storage" / "logs.txt"

async def createEmded(name:str, author:str, status:str, aboute:str, why:str, changelog:str,URL:str, bot: discord.Client)->int:
    log.config_log(level=logging.INFO)
    embed= discord.Embed(title=f"Был создан новый ПР!: 🔨{name} || ({status})", description=f"Автор: {author}\n\n Про ПР: {aboute}\n\n Почему/Баланс:{why}\n\nЧенджлог: \n {changelog}", color=0x008200, url=URL)
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
                name="Обсуждение ПРа и комментарии",
                auto_archive_duration=60
                )
                await thread.send("ECHO Servant создал успешно ветку! Ниже будут комментарии")
                logger.info('Thread created')
                return thread.id
                
async def sendToBranch(author:str,commentContent:str,idThread:int,time ,bot: discord.Client):
    log.config_log(level=logging.INFO)
    embed= discord.Embed(title=f"Было опубликовано новое сообщение от: {author}", description=f"Содержание: \n{commentContent}\nВ: ⌚{time}", color=0xffff00)
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
            await thread.send(f"Лимит символов был преодолен, коментарий передается в виде текста\n Автор:{author}\n Сообщение:{commentContent}")
            logger.info("comment sended like text")
        else:
            await thread.send(embed=embed)
            logger.info("comment sended like embed")


async def sendToPublicChangelog(changelog:str,title:str, bot: discord.Client):
    log.config_log(level=logging.INFO)
    embed= discord.Embed(title=f"Сервер получил новое обновление!\n\nЧенджлог: \n {changelog}", color=0x008200)
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
                name="Обсуждение обновления",
                auto_archive_duration=60
                )
                if(os.getenv("PUBLIC_CL_DS_ROLE")==''):
                    await thread.send("ECHO Servant создал успешно ветку! Приятного обсуждения!")
                else:
                    await thread.send(f"Обновление с названием '{title}' было опубликовано. <@&{os.getenv("PUBLIC_CL_DS_ROLE")}> приглашаются к ознакомлению с обновлением. Так же сообщаю что ветка успешно создана:3")
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