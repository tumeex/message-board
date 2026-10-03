from pydantic import BaseModel

class User(BaseModel):
    id: int = 0
    name: str = "Nameless"
    password: str = "1234"
    async def toSql(self):
        return "'{self.name}', '{self.password}'"
