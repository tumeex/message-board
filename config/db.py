from pymongo import MongoClient, AsyncMongoClient
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# MongoDB connection URI (Cloud-hosted MongoDB Atlas in this case)
uri = os.getenv("MONGO_URL")

""" Synchronous
# Create a MongoDB client
client = MongoClient(uri)
# Define database and collection
db = client["message-board"]
message_col = db["message"]
messageBoard_col = db["board"]
user_col = db["user"]
group_col = db["group"]
"""

# Async
clientAsync = AsyncMongoClient(uri)

dbAsync = clientAsync["message-board"]
message_col_async = dbAsync["message"]
messageBoard_col_async = dbAsync["board"]
user_col_async = dbAsync["user"]
group_col_async = dbAsync["group"]
