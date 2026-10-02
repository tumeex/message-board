from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from config import db
from .connection_manager import manager
from fastapi.responses import HTMLResponse
from schemas.messageSchema import list_of_serials
from views.message import m_html

from models.message import Message
from models.messageBoard import MessageBoard

router = APIRouter()

@router.websocket("/ws/recordMessage")
async def websocket_endpoint(websocket: WebSocket, client_id: str):

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            client_id = data.split(",")[0]
            message = data.split(",")[1]
            newMessage = Message({"text":message, "sender":client_id})
            # Upload to DB
            await create_message(newMessage)
    except WebSocketDisconnect:
        manager.disconnect(websocket)



# Async REST--------------------------------------------------------------------
@router.get("/messageNow")
async def get():
    return HTMLResponse(m_html)

@router.get("/messages")
async def return_messages():
        mboards = db.message_col_async.find({}, {"_id": 0})
        return await mboards.to_list()

@router.post("/messages/add")
async def create_message(message: Message):
    print("Received message/add")
    await db.message_col_async.insert_one(dict(message))
    print("Allright still")
    return {"info": "Inserted successfully"}

@router.get("/messages/{message_id}")
async def return_message(message_id: str):
    message = db.message_col_async.find_one({"id": message_id}, {"_id": 0})
    return await message

@router.get("/messages/user/{user_id}")
async def return_message(user_id: str):
    messages = db.message_col_async.find({"sender": user_id}, {"_id": 0})
    return await messages.to_list()

@router.delete("/messages/{message_id}")
async def delete_message(message_id: str):
    db.message_col.delete_one({"id": message_id})
    return {"info": "Deleted successfully"}

@router.get("/messages/addTest")
async def create_messageTest():
    bbb = Message(id="133", text="Third Message", sender="2", timestamp="2026-12-12:12:12:12:1234")
    await db.message_col_async.insert_one(dict(bbb))
    return {"info": "Inserted successfully"}
