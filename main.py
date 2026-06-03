from dotenv import load_dotenv
from fastapi import FastAPI

from routes.user_routes import user_routes

load_dotenv()

app = FastAPI()


@app.get("/")
async def health():
    return {"status": "Running perfectly..."}


app.include_router(user_routes)
