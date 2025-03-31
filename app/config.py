import os
from dotenv import load_dotenv

# Laden der Umgebungsvariabeln
load_dotenv()

# Definition der Konfigurationsvariabeln, teilw. mit Default-Wert
MDB_DATA_API_KEY = os.getenv("MDB_DATA_API_KEY")
MDB_DATA_URL = os.getenv("MDB_DATA_URL", "http://mdb-data:8001/api/v1/byName")

PORT = int(os.getenv("PORT", 8002))