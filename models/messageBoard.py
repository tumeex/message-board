from pydantic import BaseModel
from .message import Message
from .group import Group
from .user import User

class MessageBoard(BaseModel):
    id: str = None
    name: str = None
    messages: list[str] = None      # message IDs
    members: str = None             # group ID
    owner: str = None               # user ID