from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from config.dbPostgres import db
from .connection_manager import manager
from fastapi.responses import HTMLResponse
from views.user import u_html

from models.message import Message
from models.messageBoard import MessageBoard
from models.user import User

router = APIRouter()

"""
@router.websocket("/ws/getUserName/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            sendData = await return_user(user_id)
            await websocket.send_text(f"{sendData["name"]}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
"""


# Async REST--------------------------------------------------------------------

@router.get("/userNow")
async def get():
    return HTMLResponse(u_html)

@router.get("/users")
async def return_users():
    return await db.return_users()

@router.get("/user/{user_id}")
async def return_userById(user_id: int):
    return await db.return_userById(user_id)

@router.get("/user/{user_id}")
async def return_userByName(user_name: str):
    return await db.return_userByName(user_name)

@router.post("/users/add")
async def create_messageBoard(mboard: MessageBoard):
    db.user_col_async.insert_one(dict(mboard))
    return {"info": "Inserted successfully"}

@router.post("/users/login/{mboard_id}/{user}")
async def join_user(mboard_id: str, user: str):
    #await db.login_user(mboard_id, user)
    return await db.login_user(mboard_id, user)

@router.get("/users/add/addTest")
async def create_messageBoardTest():
    #db.messageBoard_col.insert_one(dict(mboard))
    bbb = MessageBoard(id="123", name="First-Board", messages=["1", "2", "3"], members="1", owner="1")
    db.user_col_async.insert_one(dict(bbb))
    return {"info": "Inserted successfully"}
