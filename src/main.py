import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.app.services import router as router_service

app = FastAPI()


@app.get("/")
def func():
    return {"message": "Welcome to the SHOP-STORE!"}


app.include_router(router_service)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
