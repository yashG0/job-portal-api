from routes.auth_routes import get_current_user
from models import Company, User, UserRole
from schema import CompanySchemaIn, CompanySchemaOut
from fastapi import APIRouter, Depends

company_routes = APIRouter()


@company_routes.post("/companies", response_model=CompanySchemaOut)
async def create_company(new_company_details:CompanySchemaIn, current_user:User = Depends(get_current_user)):
    if current_user.role == UserRole.candidate:
        