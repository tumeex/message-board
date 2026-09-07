from pydantic import BaseModel
from .user import User

class Group(BaseModel):
    id: str = None
    name: str = None
    members: list[str] = None       # user IDs