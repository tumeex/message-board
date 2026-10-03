from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from config.dbPostgres import db
from .connection_manager import manager
from fastapi.responses import HTMLResponse
from views.user import u_html

from models.message import Message
from models.messageBoard import MessageBoard
from models.user import User
from models.group import Group

router = APIRouter()


# Async REST--------------------------------------------------------------------

@router.get("/groups")
async def return_groups():
    return await db.return_groups()

@router.get("/groups/{group_id}")
async def return_group(group_id: int):
    return await db.return_group(group_id)

@router.post("/groups/add")
async def create_group(group: Group):
    return await db.create_group(group)
