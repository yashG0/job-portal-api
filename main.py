from routes.auth_routes import auth_routes
from routes.company_routes import company_routes
from fastapi import FastAPI

from routes.user_routes import user_routes

app = FastAPI()


@app.get("/")
async def health():
    return {"status": "Running perfectly..."}


app.include_router(user_routes, tags=["User Routes"])
app.include_router(company_routes, tags=["Company Routes"])
app.include_router(auth_routes, tags=["Auth Routes"])
