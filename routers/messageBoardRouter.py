from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from config import db
from .connection_manager import manager
from schemas.messageBoardSchema import list_of_serials, individual_serial
from fastapi.responses import HTMLResponse

from models.message import Message
from models.messageBoard import MessageBoard

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/123/2");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@router.websocket("/ws/{mboard_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, mboard_id: str, client_id: str):
    if await return_messageBoard(mboard_id) != None:
        print("Hallelujah")
    else:
        print("Noooooo")

    await manager.connect(websocket)
    # Let everyone know a new user joined
    await manager.broadcast(f"Client #{client_id} joined the chat")

    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast the message to all clients
            await manager.broadcast(f"Client #{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


@router.get("/messageNow")
async def get():
    return HTMLResponse(html)

@router.get("/boards")
async def return_messageBoards():
    mboards = db.messageBoard_col_async.find({}, {"_id": 0})
        #mboards2 = list_of_serials(db.messageBoard_col_async.find())
    return await mboards.to_list()

@router.get("/boards/id/{mboard_id}")
async def return_messageBoard(mboard_id: str):
    mboard = db.messageBoard_col_async.find_one({"id": mboard_id}, {"_id": 0})
    return await mboard

@router.get("/boards/id/{mboard_id}/messages")
async def return_messageBoard(mboard_id: str):
    mboard = db.messageBoard_col_async.find_one({"id": mboard_id}, {"_id": 0, "messages": 1})
    return await mboard

@router.post("/boards/add")
async def create_messageBoard(mboard: MessageBoard):
    db.messageBoard_col_async.insert_one(dict(mboard))
    return {"info": "Inserted successfully"}

@router.get("/boards/add/addTest")
async def create_messageBoardTest():
    #db.messageBoard_col.insert_one(dict(mboard))
    bbb = MessageBoard(id="123", name="First-Board", messages=["1", "2", "3"], members="1", owner="1")
    db.messageBoard_col.insert_one(dict(bbb))
    return {"info": "Inserted successfully"}
