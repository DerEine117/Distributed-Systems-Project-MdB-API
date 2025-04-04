from fastapi import FastAPI
from app.endpoints import router
from app.config import PORT

# Starten der Anwendung

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)