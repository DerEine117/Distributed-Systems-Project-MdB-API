from fastapi import APIRouter, HTTPException
import requests
from config import MDB_DATA_API_KEY, MDB_DATA_URL

router = APIRouter()

@router.get("/api/v1/getByName")
def getByName(name: str):
    params = {
        "apikey": MDB_DATA_API_KEY,
        "name": name
    }
    response = requests.get(MDB_DATA_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Fehler beim Abrufen der Daten")
    else:
        return response.json()
    
@router.get("/health")
def getHealth():
    return {"status": "ok"}