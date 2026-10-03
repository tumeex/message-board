from pydantic import BaseModel

class MessageBoard(BaseModel):
    id: int
    name: str = "Nameless"
    members: int = 0             # group ID
    owner: int = 0              # user ID
    async def toSql(self):
        return "'{self.name}', '{self.members}', '{self.owner}'"
