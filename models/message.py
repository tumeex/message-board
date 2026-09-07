from pydantic import BaseModel
from .user import User

class Message(BaseModel):
    id: str = None
    text: str = None
    sender: str = None
    timestamp: str = None