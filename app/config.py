import os
from dotenv import load_dotenv

load_dotenv()

MDB_DATA_API_KEY = os.getenv("MDB_DATA_API_KEY")
MDB_DATA_URL = os.getenv("MDB_DATA_URL", "http://mdb-data:8001/api/v1/byName")

PORT = int(os.getenv("PORT", 8002))