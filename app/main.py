from fastapi import FastAPI
from endpoints import router
from config import PORT

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=PORT)