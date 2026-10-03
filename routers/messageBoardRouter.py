from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from config.dbPostgres import db
from .connection_manager import manager
from fastapi.responses import HTMLResponse
from views.messageBoard import mb_html

from .messageRouter import create_message
from .groupRouter import create_group

from models.group import Group
from models.message import Message
from models.messageBoard import MessageBoard

router = APIRouter()

async def splitter(data: list):
    sliced = data.split(":::")
    xxx = {"mboard_id": sliced[0], "client_id": sliced[1], "message": sliced[2], "timestamp": sliced[3]}
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


@router.websocket("/ws/chatServer/room/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, user_id):
    await manager.connect(websocket)
    # Let everyone know a new user joined
    await manager.broadcast(f"Client {user_id} joined the  room {room_id}")
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
    return await db.return_messageBoards()

@router.get("/boards/{mboard_id}")
async def return_messageBoard(mboard_id: int):
    return await db.return_messageBoard(mboard_id)

@router.get("/boards/{mboard_id}/messages")
async def return_messageBoardMessages(mboard_id: int):
    return await db.return_messageBoardMessages(mboard_id)

@router.get("/boards/user/{user_id}/joined")
async def return_userJoinedMessageBoards(user_id: int):
    return await db.return_userJoinedMessageBoards(user_id)

@router.post("/boards/add")
async def create_messageBoard(mboard: MessageBoard):
    return await db.create_messageBoard(mboard)

# Initiate full shabang
@router.get("/boards/join/{mboard_id}/{user_name}")
async def join_messageBoard(mboard_id: int, user_name: str):
    user = await db.return_userByName(user_name)
    boards = await db.return_userJoinedMessageBoards(user["id"])
    groups = await db.return_groupsUser(user["id"])["id"]
    for i in groups:
        if i is not None:
            print(i)
        else:
            #newGroup = Group(members=[user_id])
            #newGroup_id = await db.create_group(newGroup)["id"]

            #newMessageBoard = MessageBoard(members=newGroup_id)
            print("Not found")
    #return await create_messageBoard(newMessageBoard, user_id, newGroup_id)
    return "HELLOO"

@router.post("/boards/{mboard_id}/messages/add")
async def create_messageToBoard(message: Message, mboard_id: int):
    db.messageBoard_col_async.update_one({"id": mboard_id}, {"$inc": {"messages": message.id}})
    return {"info": "Inserted successfully"}

@router.get("/boards/add/addTest")
async def create_messageBoardTest():
    #db.messageBoard_col.insert_one(dict(mboard))
    bbb = MessageBoard(id="123", name="First-Board", messages=["1", "2", "3"], members="1", owner="1")
    db.messageBoard_col_async.insert_one(dict(bbb))
    return {"info": "Inserted successfully"}
