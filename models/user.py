from pydantic import BaseModel

class User(BaseModel):
    id: str = None
    name: str = None
    password: str = None