from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get('/')
def func():
    return {"message": "Welcome to the SHOP-STORE!"}



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)