from pydantic import BaseModel
from datetime import datetime, timezone

class Message(BaseModel):
    id: int = 0
    text: str = "placeholder"
    sender: int = 0      # user ID
    timestamp: str = "1999-12-12 12:12:12"
    messageBoard: int = 0
    async def toSql(self):
        return f"""'{self.text}', '{self.sender}', '{self.timestamp}', '{self.messageBoard}'"""
