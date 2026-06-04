from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_db
from models import Company, Job, User
from routes.auth_routes import get_current_user
from schema import JobSchemaIn, JobSchemaOut, JobUpdateSchema

job_routes = APIRouter(prefix="/companies")


@job_routes.post(
    "/{company_id}/jobs",
    status_code=status.HTTP_201_CREATED,
    response_model=JobSchemaOut,
)
async def create_job(
    company_id: int,
    job_details: JobSchemaIn,
    current_user: User = Depends(get_current_user),
    sess: Session = Depends(get_db),
):
    company_exists = sess.scalar(
        select(Company)
        .where(Company.company_id == company_id)
        .where(Company.owner_id == current_user.user_id)
    )
    if company_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )
    if job_details.salary_max <= job_details.salary_min:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="salary_max must be greater than salary_min",
        )
    new_job = Job(
        title=job_details.title,
        description=job_details.description,
        salary_min=job_details.salary_min,
        salary_max=job_details.salary_max,
        company_id=company_id,
        job_status=job_details.job_status,
        job_type=job_details.job_type,
        work_environment=job_details.work_environment,
    )
    try:
        sess.add(new_job)
        sess.commit()
        sess.refresh(new_job)
        return new_job
    except Exception:
        sess.rollback()
        raise


@job_routes.get(
    "/{company_id}/jobs",
    status_code=status.HTTP_200_OK,
    response_model=list[JobSchemaOut],
)
async def get_jobs(
    company_id: int,
    sess: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company_exists = sess.scalar(
        select(Company)
        .where(Company.company_id == company_id)
        .where(Company.owner_id == current_user.user_id)
    )
    if company_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )
    return sess.scalars(select(Job).where(Job.company_id == company_id)).all()


@job_routes.get(
    "/jobs/{job_id}",
    status_code=status.HTTP_200_OK,
    response_model=JobSchemaOut,
)
async def get_job(
    job_id: int,
    sess: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job_exists = sess.get(Job, job_id)
    if job_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found!"
        )
    if job_exists.company.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found!"
        )
    return job_exists


@job_routes.put(
    "/jobs/{job_id}", status_code=status.HTTP_200_OK, response_model=JobSchemaOut
)
async def edit_job(
    updated_job_detail: JobUpdateSchema,
    job_id: int,
    sess: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job_exists = sess.get(Job, job_id)
    if job_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found!"
        )
    if job_exists.company.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found!"
        )
    try:
        if updated_job_detail.salary_max <= updated_job_detail.salary_min:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="salary_max must be greater than salary_min",
            )

        job_exists.title = updated_job_detail.title
        job_exists.description = updated_job_detail.description
        job_exists.salary_min = updated_job_detail.salary_min
        job_exists.salary_max = updated_job_detail.salary_max
        job_exists.job_status = updated_job_detail.job_status
        job_exists.job_type = updated_job_detail.job_type
        job_exists.work_environment = updated_job_detail.work_environment
        sess.commit()
        sess.refresh(job_exists)
        return job_exists
    except Exception:
        sess.rollback()
        raise


@job_routes.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_job(
    job_id: int,
    sess: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job_exists = sess.get(Job, job_id)
    if job_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found!"
        )
    if job_exists.company.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found!"
        )
    try:
        sess.delete(job_exists)
        sess.commit()
    except Exception:
        sess.rollback()
        raise
