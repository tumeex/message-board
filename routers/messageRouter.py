from fastapi import APIRouter, HTTPException
from config import db

from schemas.messageSchema import list_of_serials

from models.message import Message
from models.messageBoard import MessageBoard

router = APIRouter()

@router.get("/messages")
async def return_messages(): 
    messages = list_of_serials(db.message_col.find())
    return messages

@router.get("/messages/addTest")
async def create_messageTest():
    bbb = Message(id="123", text="First Message", sender="1", timestamp="2026-12-12:12:12:12:1234")
    db.message_col.insert_one(dict(bbb))
    return {"info": "Inserted successfully"}

@router.post("/messages/add")
async def create_message(message: Message):
    db.messageBoard_col.insert_one(dict(message))
    return {"info": "Inserted successfully"}

@router.get("/messages/id/{message_id}")
async def return_message(message_id: str) -> Message: 
    message = list_of_serials(await db.message_col.find_one({"id": message_id}))
    if message != None:
        return message
    else:
        return {"message": "Not Found"}

@router.delete("/messages/id/{message_id}")
async def delete_message(message_id: str):
    db.message_col.delete_one({"id": message_id})
    return {"info": "Deleted successfully"}