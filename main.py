from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from api.user_api import user_routes

app = FastAPI()


@app.get("/")
async def health():
    return {"status": "Running perfectly..."}


app.include_router(user_routes)
