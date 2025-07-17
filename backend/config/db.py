from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # ✅ Make sure this is here BEFORE using os.getenv

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["medical"]
report_collection = db["report"]
