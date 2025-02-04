import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.app.services import router as router_service
from src.app.auth import router as router_auth
from src.app.categories import router as router_category
from src.app.customers import router as router_customer
from src.app.managers import router as router_manager
from src.app.regions import router as router_region
from src.app.products import router as router_product

app = FastAPI()


@app.get("/")
def func():
    return {"message": "Welcome to the SHOP-STORE!"}


app.include_router(router_auth)
app.include_router(router_service)
app.include_router(router_category)
app.include_router(router_product)
app.include_router(router_manager)
app.include_router(router_region)
app.include_router(router_customer)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="localhost")
