from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# MongoDB connection URI (Cloud-hosted MongoDB Atlas in this case)
uri = os.getenv("MONGO_URL")

# Create a MongoDB client
client = MongoClient(uri)

# Define database and collection
db = client["message-board"]
message_col = db["message"]
messageBoard_col = db["board"]
user_col = db["user"]
group_col = db["group"]