from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_db
from models import Company, User, UserRole
from routes.auth_routes import get_current_user
from schema import CompanySchemaIn, CompanySchemaOut

company_routes = APIRouter()


@company_routes.post(
    "/companies", response_model=CompanySchemaOut, status_code=status.HTTP_201_CREATED
)
async def create_company(
    new_company_details: CompanySchemaIn,
    current_user: User = Depends(get_current_user),
    sess: Session = Depends(get_db),
):
    try:
        if current_user.role == UserRole.candidate:
            current_user.role = UserRole.employer
            sess.commit()

        company_exists = sess.scalar(
            select(Company).where(Company.name == new_company_details.name)
        )
        if company_exists is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Company {new_company_details.name} already exists!",
            )

        new_company = Company(
            name=new_company_details.name,
            description=new_company_details.description,
            owner_id=current_user.user_id,
        )

        sess.add(new_company)
        sess.commit()
        sess.refresh(new_company)
        return new_company

    except Exception:
        sess.rollback()
        raise


@company_routes.get(
    "/companies", response_model=list[CompanySchemaOut], status_code=status.HTTP_200_OK
)
async def get_companies(
    sess: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return sess.scalars(
        select(Company).where(Company.owner_id == current_user.user_id)
    ).all()


@company_routes.get(
    "/companies/{company_id}",
    response_model=CompanySchemaOut,
    status_code=status.HTTP_200_OK,
)
async def get_company(
    company_id: int,
    sess: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company = sess.scalar(
        select(Company)
        .where(Company.owner_id == current_user.user_id)
        .where(Company.company_id == company_id)
    )

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )

    return company
