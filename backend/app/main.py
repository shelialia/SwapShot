from fastapi import FastAPI
from app.routers.transactions import router
from fastapi.middleware.cors import CORSMiddleware
import threading
from app.cache.transaction_cache import (
    update_cache_periodically,
)  # Import the cache updater


app = FastAPI()
app.include_router(router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
def start_cache_updater():
    cache_updater_thread = threading.Thread(target=update_cache_periodically)
    cache_updater_thread.daemon = (
        True  # Ensures the thread closes when the app shuts down
    )
    cache_updater_thread.start()
