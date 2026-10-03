from pydantic import BaseModel

class Group(BaseModel):
    id: int = 0
    name: str = "Nameless"
    members: list[int] = [0]       # user IDs
    async def toSql(self):
        return "'{self.name}', '{self.members}', '{self.owner}'"
