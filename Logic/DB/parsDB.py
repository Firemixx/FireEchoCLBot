import sqlite3 as sq 
import asyncio
import aiosqlite
from pathlib import Path
import logging
from Logic import logging as log


logger=logging.getLogger(__name__)
pr_db_path = Path(__file__).resolve().parents[2] / "Storage" / "pullrequests.db"

comm_db_path = Path(__file__).resolve().parents[2] / "Storage" / "comments.db"

async def Init():
    log.config_log(level=logging.INFO)
    async with aiosqlite.connect(pr_db_path) as db:
        curs= await db.cursor()
        initCommandPRs="""
        CREATE TABLE IF NOT EXISTS pullrequests(
            idPR INTEGER NOT NULL,
            isClosed BOOLEAN DEFAULT FALSE,
            idDSThread INTEGER
        );
        """
        await curs.execute(initCommandPRs)
        await db.commit()
        await db.close()

    async with aiosqlite.connect(comm_db_path) as dbcomm:
        CommCurs= await dbcomm.cursor()
        initCommandComments="""
        CREATE TABLE IF NOT EXISTS comments(
            idComment INTEGER
        );
        """
        await CommCurs.execute(initCommandComments)
        await dbcomm.commit()
        await dbcomm.close()
    logger.info("Initializing of DB ended")

async def addToDBPR(idPR:int,isClosed:bool,DSThread:int):
    log.config_log(level=logging.INFO)
    async with aiosqlite.connect(pr_db_path) as db:
        await db.execute("""
        INSERT INTO pullrequests(idPR,isClosed,idDSThread)
        VALUES (?,?,?);
                        """,(idPR,isClosed,DSThread)
                         )
        await db.commit()
        await db.close()
        logger.info(f"id:{idPR}, is closed:{isClosed}, DS Thread:{DSThread} was added to DB")

async def addToDBComm(idComm:int):
    log.config_log(level=logging.INFO)
    async with aiosqlite.connect(comm_db_path) as db:
        await db.execute("""
        INSERT INTO comments(idComment)
        VALUES (?);
                        """,(idComm,)
                         )
        await db.commit()
        await db.close()
        logger.info(f"{idComm} comment was added to DB")

async def findNotClosed()->dict:
    log.config_log(level=logging.INFO)
    logger.info("Start finding not closed")
    dictToReturn={} # id of message and url to pr
    async with aiosqlite.connect(pr_db_path) as db:
        async with db.execute(f"""SELECT * FROM pullrequests WHERE isClosed = false;""") as cursor:
            async for rows in cursor:
                message=rows[2]
                id=rows[0]
                dictToReturn.update({id:message})
    await db.close()
    logger.info("Ended finding not closed PR's")
    return dictToReturn

async def isPostedComment(id:int)->bool:
    log.config_log(level=logging.INFO)
    logger.info(f"Check comment with ID{id}")
    async with aiosqlite.connect(comm_db_path) as db:
        async with db.execute(f"""SELECT * FROM comments WHERE idComment = ?;""",(id,)) as cursor:
            res=await cursor.fetchone()
            if (res==None):
                logger.info("Comment not posted")
                return True
            else:
                logger.warning("Comment is already posted!")
                return False

