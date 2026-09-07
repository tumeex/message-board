from fastapi import APIRouter, HTTPException
from config import db

from schemas.userSchema import list_of_serials

from models.message import Message
from models.messageBoard import MessageBoard
from models.user import User

router = APIRouter()