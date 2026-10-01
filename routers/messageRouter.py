from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from config import db

from schemas.messageSchema import list_of_serials

from models.message import Message
from models.messageBoard import MessageBoard

router = APIRouter()


@router.get("/messages")
async def return_messages():
        mboards = db.message_col_async.find({}, {"_id": 0})
        return await mboards.to_list()

@router.get("/messages/addTest")
async def create_messageTest():
    bbb = Message(id="133", text="Third Message", sender="2", timestamp="2026-12-12:12:12:12:1234")
    await db.message_col_async.insert_one(dict(bbb))
    return {"info": "Inserted successfully"}

@router.post("/messages/add")
async def create_message(message: Message):
    await db.message_col_async.insert_one(dict(message))
    return {"info": "Inserted successfully"}

@router.get("/messages/id/{message_id}")
async def return_message(message_id: str):
    message = db.message_col_async.find_one({"id": message_id}, {"_id": 0})
    return await message

@router.delete("/messages/id/{message_id}")
async def delete_message(message_id: str):
    db.message_col.delete_one({"id": message_id})
    return {"info": "Deleted successfully"}
