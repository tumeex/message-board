from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from config import db
from .connection_manager import manager
from schemas.messageBoardSchema import list_of_serials, individual_serial
from fastapi.responses import HTMLResponse
from views.messageBoard import mb_html
from .messageRouter import create_message

from models.message import Message
from models.messageBoard import MessageBoard

router = APIRouter()

async def splitter(data: str):
    xxx = {"mboard_id": data.split(",")[0], "client_id": data.split(",")[1], "message": data.split(",")[2], "timestamp": data.split(",")[3]}
    #print(xxx)
    return xxx

@router.websocket("/ws/chatServer")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    # Let everyone know a new user joined
    await manager.broadcast(f"New client joined the chat")
    messageDB = []
    try:
        while True:
            data = await websocket.receive_text()
            content = await splitter(data)
            # Broadcast the message to all clients
            await manager.broadcast(f"Room: {content["mboard_id"]}-Client {content["client_id"]}: {content["message"]}")
            messageDB.append(content)

    except WebSocketDisconnect:
        print("Closed")
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{content["client_id"]} left the chat")

    finally:
        affirmedList = []
        for i in messageDB:
            print(i)
            #await create_message(i)

        print("message/req finished here")


# Async REST--------------------------------------------------------------------
@router.get("/messageBoardNow")
async def get():
    return HTMLResponse(mb_html)

@router.get("/boards")
async def return_messageBoards():
    mboards = db.messageBoard_col_async.find({}, {"_id": 0})
        #mboards2 = list_of_serials(db.messageBoard_col_async.find())
    return await mboards.to_list()

@router.get("/boards/{mboard_id}")
async def return_messageBoard(mboard_id: str):
    mboard = db.messageBoard_col_async.find_one({"id": mboard_id}, {"_id": 0})
    return await mboard

@router.get("/boards/{mboard_id}/messages")
async def return_messageBoard(mboard_id: str):
    mboard = db.messageBoard_col_async.find_one({"id": mboard_id}, {"_id": 0, "messages": 1})
    return await mboard

@router.get("/boards/user/{user_id}/joined")
async def return_userJoinedMessageBoards():
    groups = db.group_col_async.find({"members": { "$in": [user_id]}}, {"_id": 0})
    return await groups.to_list()

@router.get("/boards/user/{user_id}/owned")
async def return_userOwnedMessageBoards():
    mboards = db.messageBoard_col_async.find({"owner": user_id}, {"_id": 0})
    return await mboards.to_list()

@router.post("/boards/add")
async def create_messageBoard(mboard: MessageBoard):
    db.messageBoard_col_async.insert_one(dict(mboard))
    return {"info": "Inserted successfully"}

@router.post("/boards/{mboard_id}/messages/add")
async def create_messageToBoard(message: Message, mboard_id: str):
    db.messageBoard_col_async.update_one({"id": mboard_id}, {"$inc": {"messages": message.id}})
    return {"info": "Inserted successfully"}

@router.get("/boards/add/addTest")
async def create_messageBoardTest():
    #db.messageBoard_col.insert_one(dict(mboard))
    bbb = MessageBoard(id="123", name="First-Board", messages=["1", "2", "3"], members="1", owner="1")
    db.messageBoard_col_async.insert_one(dict(bbb))
    return {"info": "Inserted successfully"}
