from fastapi import APIRouter, HTTPException
import requests
from app.config import MDB_DATA_API_KEY, MDB_DATA_URL

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
        data = response.json()
        if "data" not in data:
            raise HTTPException(status_code=500, detail="Invalid response from MDB-Data")

        if data.get("records", 0) == 0:
            raise HTTPException(status_code=204)

        filtered_data = [{"id": record["id"], "titel": record["titel"]} for record in data["data"]]

        return filtered_data
        #return response.json()
    
@router.get("/health")
def getHealth():
    return {"status": "bestens"}