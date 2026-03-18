import aiohttp
from bs4 import BeautifulSoup as bs
from bs4.element import Tag, ResultSet
import discord
import requests
import asyncio
import os
import logging
from dotenv import load_dotenv, set_key
from Logic.DS import MessageMenager as ds
from Logic import logging as log
import time
from fake_useragent import UserAgent
from pathlib import Path
from Logic.DB import parsDB as db

logger=logging.getLogger(__name__)
HEADERS={"User-Agent":UserAgent().random}
env_path = Path(__file__).resolve().parents[2] / "Storage" / ".env"

async def parsPR(bot: discord.Client):
    log.config_log(level=logging.INFO)
    async with aiohttp.ClientSession() as session:
        load_dotenv(env_path, override=True)
        number_pr = int(os.getenv("NUMBER_OF_PR"))
        url = os.getenv("REPO_URL")
        if (bool(os.getenv("IS_PARS"))):
            pullURL=f"{url}/pull/{number_pr}"
            logger.info(f"Processing {pullURL}")
            async with session.get(pullURL, headers=HEADERS) as reqPull:
                if reqPull.status!=200:
                    return
                tree = await reqPull.text()
                soup = bs(tree, 'lxml')
                namePR=soup.find('span', {'class':'Text__StyledText-sc-1klmep6-0 f1 text-normal markdown-title prc-Text-Text-9mHv3'})
                author=soup.find('div',{'class':'d-flex flex-items-center flex-wrap gap-1'}).find('strong').find('a')
                descriptionOfPR= soup.find('div', {'class':'comment-body markdown-body js-comment-body soft-wrap user-select-contain d-block'})
                ulInDescr=descriptionOfPR.find('ul', {'dir':'auto'})
                aboutePR=descriptionOfPR.find_all('p', {'dir':'auto'})
                if (ulInDescr!=None):
                    changelogOfPR= ulInDescr.find('li')
                else:
                    changelogOfPR=""
                status=soup.find('span',{"class":"prc-StateLabel-StateLabel-Iawzp flex-self-start"}).text
                if (status=='Closed' or status=='Merged' or status=='Draft'):
                    boolenStatus=True
                elif(status=='Open'):
                    boolenStatus=False
                name,descr,changelog=await checkAndSolve([namePR,aboutePR,changelogOfPR])
                id = await ds.createEmded(name,author.text,descr,changelog, pullURL,status, bot)
                await db.addToDBPR(number_pr,boolenStatus,id)

                number_pr += 1

                set_key(env_path, 'NUMBER_OF_PR', str(number_pr))

async def parsComments(bot: discord.Client):
    log.config_log(level=logging.INFO)
    async with aiohttp.ClientSession() as session:
        dictionary=await db.findNotClosed()
        for id,thread in dictionary.items():
            async with session.get(f"https://api.github.com/repos/SS14EchoProtocol/Echo-Protocol-SS14/issues/{id}/comments", headers=HEADERS) as commJSON:
                data=await commJSON.json()
                if isinstance(data, dict):
                    if data.get("message") == "Not Found" or data.get("message")== "API rate limit exceeded for 194.12.74.5. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)":
                        continue
                for comment in data:
                    author = comment["user"]["login"]
                    content= comment["body"]
                    idComm= comment["id"]
                    if author != "github-actions[bot]":
                        if(await db.isPostedComment(idComm)):
                            await ds.sendToBranch(author,content,thread, bot)
                            await db.addToDBComm(idComm)
                        else:
                            continue

async def checkAndSolve(blocklist: list):
    listOfTexts=[]
    for i in blocklist:
        match i:
            case Tag():
                listOfTexts.append(i.text)
            
            case ResultSet():
                listOfTexts.append("\n".join(tag.text for tag in i))

            case None:
                listOfTexts.append("")

            case _:
                listOfTexts.append(str(i))
    return tuple(listOfTexts)