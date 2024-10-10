from fastapi import FastAPI
from .routers import transactions

app = FastAPI()

# Include the transaction routes
app.include_router(transactions.router)
