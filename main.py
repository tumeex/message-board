from fastapi import FastAPI, HTTPException
#from pydantic import BaseModel
from routers import userRouter, messageBoardRouter, messageRouter
from contextlib import asynccontextmanager
from config.dbPostgres import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verify connection when the application starts
    await db.connect()
    print("Connected to Postgres")
    yield
    # Close connection when the application stops
    await db.disconnect()

app = FastAPI(
    title="Message Board",
    description="This is description",
    version="0.1.0",
    lifespan=lifespan
)
"""
@app.on_event("startup")
def startup_event():
    # Create db and tables
    print("App started")
@app.on_event("shutdown")
def shutdown_event():
    # Delete db and tables
    print("App ended")
"""

app.include_router(userRouter.router)
app.include_router(messageBoardRouter.router)
app.include_router(messageRouter.router)

@app.get("/")
async def root():
    return {"Hello": "World"}

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
