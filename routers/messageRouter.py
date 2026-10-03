from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from config.dbPostgres import db, getTime
from .connection_manager import manager
from fastapi.responses import HTMLResponse
from views.message import m_html

from models.message import Message
from models.messageBoard import MessageBoard

router = APIRouter()

@router.websocket("/ws/welcome")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    # Let everyone know a new user joined
    time = await getTime()
    await manager.broadcast(f"{time}: New client joined the waiting room")
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast the message to all clients
            await manager.broadcast(f"{data}")
    except WebSocketDisconnect:
        print("Visitor closed")
        manager.disconnect(websocket)
        await manager.broadcast(f"Visitor left the chat")
    finally:
        print("Visitor WS finally ended")


# Async REST--------------------------------------------------------------------
@router.get("/messageNow")
async def get():
    return HTMLResponse(m_html)

@router.get("/messages")
async def return_messages():
    return await db.return_messages()

@router.get("/messages/{message_id}")
async def return_message(message_id: int):
    message = db.message_col_async.find_one({"id": message_id}, {"_id": 0})
    return await message

@router.post("/messages/add")
async def create_message(message: Message):
    print("Received message/add")
    return await db.create_message(message)

@router.get("/messages/user/{user_id}")
async def return_userMessages(user_id: int):
    messages = db.message_col_async.find({"sender": user_id}, {"_id": 0})
    return await messages.to_list()

@router.delete("/messages/{message_id}")
async def delete_message(message_id: int):
    db.message_col.delete_one({"id": message_id})
    return {"info": "Deleted successfully"}

@router.get("/messages/addTest")
async def create_messageTest():
    bbb = Message(id="133", text="Third Message", sender="2", timestamp="2026-12-12:12:12:12:1234")
    await db.message_col_async.insert_one(dict(bbb))
    return {"info": "Inserted successfully"}
