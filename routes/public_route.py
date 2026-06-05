from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from db import get_db
from models import Job, JobSortSchema, JobType, WorkEnvironment
from schema import JobSchemaOut

public_route = APIRouter(tags=["Public Routes"])


@public_route.get(
    "/jobs", response_model=list[JobSchemaOut], status_code=status.HTTP_200_OK
)
async def get_all_jobs(
    keyword: str | None = None,
    job_type: JobType | None = None,
    work_environment: WorkEnvironment | None = None,
    sort: JobSortSchema = JobSortSchema.newest,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=5, ge=1, le=100),
    sess: Session = Depends(get_db),
):
    offset = (page - 1) * size

    query = select(Job)
    if keyword:
        query = query.where(
            or_(Job.title.ilike(f"%{keyword}%"), Job.description.ilike(f"%{keyword}%"))
        )
    if job_type:
        query = query.where(Job.job_type == job_type)
    if work_environment:
        query = query.where(Job.work_environment == work_environment)

    if sort == JobSortSchema.newest:
        query = query.order_by(Job.created_at.desc())

    elif sort == JobSortSchema.salary_desc:
        query = query.order_by(Job.salary_max.desc(), Job.job_id.desc())

    elif sort == JobSortSchema.salary_asc:
        query = query.order_by(Job.salary_min.asc())

    return sess.scalars(query.offset(offset).limit(size)).all()


@public_route.get(
    "/jobs/{job_id}", response_model=JobSchemaOut, status_code=status.HTTP_200_OK
)
async def get_job(job_id: int, sess: Session = Depends(get_db)):
    job_exists = sess.get(Job, job_id)
    if job_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not Found!"
        )
    return job_exists
