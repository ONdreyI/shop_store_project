import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))


app = FastAPI()


@app.get('/')
def func():
    return {"message": "Welcome to the SHOP-STORE!"}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
