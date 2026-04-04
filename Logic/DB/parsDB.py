import asyncio
from typing import Any
from sqlalchemy import JSON
from sqlalchemy import select,update,delete,func
from sqlalchemy.orm import Mapped,DeclarativeBase,mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs,async_sessionmaker,create_async_engine
from pathlib import Path
import logging
from Logic import logging as log


logger=logging.getLogger(__name__)
engine=create_async_engine(url='sqlite+aiosqlite:///Storage/db.sqlite3', echo=True)
async_session=async_sessionmaker(bind=engine,expire_on_commit=False)

class Base(AsyncAttrs,DeclarativeBase):
    type_annotation_map = {
        dict[str, str]: JSON,
        dict: JSON 
    }

class PR(Base):
    __tablename__= 'PRs'
    id:Mapped[int] = mapped_column(primary_key=True)
    threadId:Mapped[int] = mapped_column(nullable=False)
    info:Mapped[dict[str, str]] = mapped_column()
    isClosed:Mapped[bool]
    isMerged:Mapped[bool]

class Comment(Base):
    __tablename__= 'Comments'
    id:Mapped[int] = mapped_column(primary_key=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)




async def addPR(id:int,info:dict,threadId:int,isClosed:bool,isMerged:bool):
    async with async_session() as s:
        pr= await s.scalar(select(PR).where(PR.id==id))
        if pr:
            return
        else:
            new_pr=PR(id=id,info=info,threadId=threadId,isClosed=isClosed,isMerged=isMerged)
            s.add(new_pr)
            await s.commit()
            await s.refresh(new_pr)
            logger.info(f"Added new PR to DB!")
            return(new_pr)
        
async def addComment(id:int):
    async with async_session() as s:
        comm= await s.scalar(select(Comment).where(Comment.id==id))
        if comm:
            return
        else:
            new_comm=Comment(id=id)
            s.add(new_comm)
            await s.commit()
            await s.refresh(new_comm)
            logger.info(f"Added new comment to DB!")
            return(new_comm)


async def isPostedComm(id:int):
    async with async_session() as s:
        comm= await s.scalar(select(Comment).where(Comment.id==id))
        if comm:
            logger.info(f"Comment with ID:{id} is already posted!")
            return True
        else:
            logger.info(f"Comment with ID:{id} newer posted!")
            return False

async def findNotClosed()->list:
    dictToReturn={}
    async with async_session() as s:
        pr= await s.scalars(select(PR).where(PR.isClosed==False))
        if pr:
            for row in pr:
                id=row.id
                thread=row.threadId
                dictToReturn.update({id:thread})
        return dictToReturn
    
async def findNotMerged()->list:
    dictToReturn={}
    async with async_session() as s:
        pr= await s.scalars(select(PR).where(PR.isMerged==False))
        if pr:
            for row in pr:
                id=row.id
                thread=row.threadId
                dictToReturn.update({id:thread})
            return dictToReturn
        else:
            logger.warning("Not merged PR's was not found!")
            
        
async def makeMerged(id:int):
    async with async_session() as s:
        pr= await s.execute(update(PR).where(PR.id==id).values(isMerged=True))
        await s.commit()
        logger.info(f"PR with ID:{id} made merged!")

async def getBody(id:int):
    async with async_session() as s:
        pr= await s.scalar(select(PR).where(PR.id==id))
        logger.info(f"Collected body of PR with ID:{id}")
        return pr.info
