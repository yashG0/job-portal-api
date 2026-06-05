from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_db
from models import Application, Job, JobApplicationStatus, User, UserRole
from routes.auth_routes import get_current_user
from schema import ApplicationSchemaIn, ApplicationSchemaOut

application_routes = APIRouter()


@application_routes.post(
    "/jobs/{job_id}/apply",
    response_model=ApplicationSchemaOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_application(
    job_id: int,
    application_detail: ApplicationSchemaIn,
    sess: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.candidate:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only Candidate apply!"
        )

    existing_job = sess.get(Job, job_id)
    if existing_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found!"
        )
    existing_application = sess.scalar(
        select(Application)
        .where(Application.job_id == existing_job.job_id)
        .where(Application.user_id == current_user.user_id)
    )
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User Already Applied!"
        )
    new_application = Application(
        job_id=existing_job.job_id,
        user_id=current_user.user_id,
        resume_url=application_detail.resume_url,
        status=JobApplicationStatus.submitted,
    )
    try:
        sess.add(new_application)
        sess.commit()
        sess.refresh(new_application)
        return new_application
    except Exception:
        sess.rollback()
        raise


@application_routes.get(
    "/applications/me",
    status_code=status.HTTP_200_OK,
    response_model=list[ApplicationSchemaOut],
)
async def get_my_applications(
    current_user: User = Depends(get_current_user), sess: Session = Depends(get_db)
):
    if current_user.role != UserRole.candidate:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Candidate can see applications!",
        )
    return sess.scalars(
        select(Application).where(Application.user_id == current_user.user_id)
    ).all()


@application_routes.get(
    "/jobs/{job_id}/applications",
    status_code=status.HTTP_200_OK,
    response_model=list[ApplicationSchemaOut],
)
async def get_job_applications(
    job_id: int,
    current_user: User = Depends(get_current_user),
    sess: Session = Depends(get_db),
):
    job_exist = sess.get(Job, job_id)
    if job_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found!"
        )
    if job_exist.company.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job not found!"
        )

    return sess.scalars(select(Application).where(Application.job_id == job_id)).all()


@application_routes.patch(
    "/applications/{application_id}/status",
    response_model=ApplicationSchemaOut,
    status_code=status.HTTP_200_OK,
)
async def change_status(
    job_status: JobApplicationStatus,
    application_id: int,
    current_user: User = Depends(get_current_user),
    sess: Session = Depends(get_db),
):
    if current_user.role != UserRole.employer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Employer only route!"
        )

    application_exists = sess.get(Application, application_id)
    if application_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Application not found!"
        )
    if application_exists.job.company.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Application not found!"
        )
    try:
        application_exists.status = job_status
        sess.commit()
        sess.refresh(application_exists)
        return application_exists
    except Exception:
        sess.rollback()
        raise
