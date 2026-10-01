from fastapi import FastAPI, HTTPException
#from pydantic import BaseModel
from routers import userRouter, messageBoardRouter, messageRouter
from contextlib import asynccontextmanager
from config import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verify connection when the application starts
    await db.clientAsync.admin.command("ping")
    print("Connected to MongoDB")
    yield
    # Close connection when the application stops
    await db.clientAsync.close()

app = FastAPI(
    title="Message Board",
    description="This is description",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(userRouter.router)
app.include_router(messageBoardRouter.router)
app.include_router(messageRouter.router)

"""
class Message(BaseModel):
    id: int = None
    text: str = None
    sender: str = None

class MessageBoard(BaseModel):
    id: int = None
    name: str = None
    messages: list[Message] = None

mess1 = Message(id=1, text="Hello1", sender="Ano1")
mess2 = Message(id=2, text="Hello2", sender="Ano2")
mess3 = Message(id=3, text="Hello3", sender="Ano3")
mboard1 = MessageBoard(id=1, name="Board1", messages=[mess1, mess2, mess3])
mboard2 = MessageBoard(id=2, name="Board2", messages=[mess1, mess2])
mboard3 = MessageBoard(id=3, name="Board3", messages=[mess2, mess3])

mboards = [mboard1, mboard2, mboard3]
"""

@app.get("/")
async def root():
    return {"Hello": "World"}
