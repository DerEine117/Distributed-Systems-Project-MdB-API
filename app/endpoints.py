from fastapi import APIRouter, HTTPException
import requests
from app.config import MDB_DATA_API_KEY, MDB_DATA_URL

router = APIRouter()

# Festlegen des Endpunkts und der HTTP-Methode
@router.get("/api/v1/getByName")
def getByName(name: str):
    params = {
        "apikey": MDB_DATA_API_KEY,
        "name": name
    }
    try:
        response = requests.get(MDB_DATA_URL, params=params, timeout=2)
        # Überprüfen des Status-Codes der Antwort
        if response.status_code == 401:
            raise HTTPException(status_code=response.status_code, detail="ERROR: Invalid credentials")
        elif response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error: INTERNAL SERVER ERROR")
        else:
            # Überprüfen des Inhalts der Antwort
            data = response.json()
            if "data" not in data:
                raise HTTPException(status_code=500, detail="ERROR: INTERNAL SERVER ERROR")

            if data.get("records", 0) == 0:
                raise HTTPException(status_code=204)
            # Filtern der Daten; nur angefordertes zurückgeben
            filtered_data = [{"id": record["id"], "titel": record["titel"]} for record in data["data"]]

            return filtered_data
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="ERROR: Timeout")
    
# Festlegen des Endpunkts und der HTTP-Methode
@router.get("/health")
def getHealth():
    # Rückgabe eines Status-Codes 200
    return {"status": "bestens"}