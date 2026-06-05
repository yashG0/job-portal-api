from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_db
from models import Job
from schema import JobSchemaOut

public_route = APIRouter(tags=["Public Routes"])


@public_route.get(
    "/jobs", response_model=list[JobSchemaOut], status_code=status.HTTP_200_OK
)
async def get_all_jobs(sess: Session = Depends(get_db)):
    return sess.scalars(select(Job)).all()


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
