from fastapi import APIRouter, HTTPException
from config import db
from schemas.messageBoardSchema import list_of_serials

from models.message import Message
from models.messageBoard import MessageBoard

router = APIRouter()

@router.get("/boards")
async def return_messageBoards(): 
    mboards = await list_of_serials(db.messageBoard_col.find())
    return mboards

@router.get("/boards/id/{mboard_id}")
async def return_messageBoard(mboard_id: str) -> MessageBoard: 
    mboards = await return_messageBoards()
    for i in mboards:
        if i.id == mboard_id:
            return i
    return {"message": "Not Found"}

@router.post("/boards")
async def create_messageBoard(mboard: MessageBoard):
    db.messageBoard_col.insert_one(dict(mboard))
    return {"info": "Inserted successfully"}


@router.get("/boards/addTest")
async def create_messageBoardTest():
    #db.messageBoard_col.insert_one(dict(mboard))
    bbb = MessageBoard(id="123", name="First-Board", messages=["1", "2", "3"], members="1", owner="1")
    db.messageBoard_col.insert_one(dict(bbb))
    return {"info": "Inserted successfully"}
