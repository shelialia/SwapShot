from fastapi import FastAPI
from app.routers.transactions import router


app = FastAPI()
app.include_router(router)