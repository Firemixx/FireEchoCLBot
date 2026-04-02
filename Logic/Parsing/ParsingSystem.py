import aiohttp
import discord
import requests
import asyncio
import os
import logging
import re
from github import Github
from dotenv import load_dotenv, set_key
from Logic.DS import MessageMenager as ds
from Logic import logging as log
from pathlib import Path
from Logic.DB import parsDB as db

logger=logging.getLogger(__name__)
env_path = Path(__file__).resolve().parents[2] / "Storage" / ".env"
load_dotenv(env_path)

async def parsPR(bot: discord.Client):
    log.config_log(level=logging.INFO)
    load_dotenv(env_path, override=True)
    g=Github(os.getenv("GIT_TOKEN"))
    repo=g.get_repo(os.getenv("REPO_PATH"))
    pullrequest=repo.get_pull(int(os.getenv("NUMBER_OF_PR")))
    title=pullrequest.title
    author=pullrequest.user.login
    isMerged=pullrequest.merged
    status=pullrequest.state
    descr=pullrequest.body
    repackedDescr=await repackText(descr)

    statusToDS=''
    match(isMerged):
        case True:
            statusToDS='Merged'
        case False:
            if status=='closed':
                statusToDS='Closed'
            elif status=='open':
                statusToDS='Open'
    boolenIsClosed=False
    match (status):
        case 'closed':
            boolenIsClosed = True
        case 'open':
            boolenIsClosed = False
    print(repackedDescr)
    if "Чейнджлог" not in repackedDescr:
        repackedDescr.update({'Чейнджлог':'Чейнджлог отсутствует'})
        logger.warning("Changelog is missing")
    if "Описание PR" not in repackedDescr:
        repackedDescr.update({'Описание PR':'Описание отсутствует'})
        logger.warning("Description is missing")
    if "Почему / Баланс" not in repackedDescr:
        repackedDescr.update({'Почему / Баланс':'Описание причины добавления отсутствует'})
        logger.warning("Why/Balance is missing")
    url=f'https://github.com/{os.getenv("REPO_PATH")}/pull/{int(os.getenv("NUMBER_OF_PR"))}'
    id = await ds.createEmded(title,author,statusToDS,repackedDescr['Описание PR'],repackedDescr['Почему / Баланс'], repackedDescr['Чейнджлог'],url, bot )
    await db.addPR(int(os.getenv("NUMBER_OF_PR")),repackedDescr,id,boolenIsClosed, isMerged)
    set_key(env_path,'NUMBER_OF_PR', str(int(os.getenv("NUMBER_OF_PR"))+1))
    


async def repackText(text:str):
    log.config_log(level=logging.INFO)
    repacked_text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)

    repacked_text = re.sub(r"# ❗❗.*", "", repacked_text)
    repacked_text = re.sub(r"\r.*","",repacked_text)
    repacked_text = re.sub(r"add:","🆕",repacked_text)
    repacked_text = re.sub(r"tweak:","🔧",repacked_text)
    repacked_text = re.sub(r"fix:","🐛",repacked_text)
    repacked_text = re.sub(r"remove:","🛑",repacked_text)
    repacked_text = re.sub(r"^\s*- \[[x ]\].*$", "", repacked_text, flags=re.MULTILINE)
    repacked_text = re.sub(r"\n{3,}", "\n\n", repacked_text)
    repacked_text = re.sub(r'<img[^>]*src="([^"]+)"[^>]*>',r'\1',repacked_text)
    sections = re.split(r"\n(?=## )", repacked_text.strip())
    
    result = {}
    for section in sections:
        lines = section.split('\n', 1)
        if len(lines) > 1:
            title = lines[0].replace('##', '').strip()
            content = lines[1].strip()
            if content:
                result[title] = content
    logger.info("Repacking ended!")
    return result

async def parsComments(bot:discord.Client):
    log.config_log(level=logging.INFO)
    dictOfNotClosed=await db.findNotClosed()
    for id,thread in dictOfNotClosed.items():
        g=Github(os.getenv("GIT_TOKEN"))
        repo=g.get_repo(os.getenv("REPO_PATH"))
        pullrequest=repo.get_pull(id)
        comments=pullrequest.get_comments()
        for i in comments:
            idComm=i.id
            if (await db.isPostedComm(idComm)):
                continue
            author=i.user.login
            body=i.body
            time=i.created_at
            await db.addComment(idComm)
            await ds.sendToBranch(author,body,thread,time,bot)
            logger.info(f"Sended to branch with ID{thread} comment with ID:{idComm}!")

async def checkUpMerged(bot:discord.Client):
    dictOfNotMerged=await db.findNotMerged()
    for id,thread in dictOfNotMerged.items():
        g=Github(os.getenv("GIT_TOKEN"))
        repo=g.get_repo(os.getenv("REPO_PATH"))
        pullrequest=repo.get_pull(id)  
        isMerged=pullrequest.merged
        if(isMerged):
            await db.makeMerged(id)
            body=await db.getBody(id)

            changelog=body['Чейнджлог']
            await ds.sendToPublicChangelog(changelog,bot)
            logger.info(f"Sended to public CL with ID{id}")
        else:
            continue
