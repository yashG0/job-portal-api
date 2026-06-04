from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from models import JobStatus, JobType, UserRole, WorkEnvironment


class UserSchemaBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserSchemaIn(UserSchemaBase):
    password: str = Field(min_length=6, max_length=255)


class UserSchemaOut(UserSchemaBase):
    user_id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime


class PasswordUpdate(BaseModel):
    old_password: str = Field(min_length=6, max_length=255)
    new_password: str = Field(min_length=6, max_length=255)


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CompanySchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CompanySchemaIn(CompanySchemaBase):
    name: str = Field(min_length=3, max_length=50)
    description: str | None = Field(default=None)


class CompanySchemaOut(CompanySchemaIn):
    company_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime


class CompanyEditSchema(CompanySchemaBase):
    name: str = Field(max_length=50, min_length=3)
    description: str


class JobSchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class JobSchemaIn(JobSchemaBase):
    title: str = Field(min_length=3, max_length=100)
    description: str
    salary_min: int = Field(gt=10000)
    salary_max: int
    job_status: JobStatus = Field(default=JobStatus.opened)
    job_type: JobType = Field(default=JobType.full_time)
    work_environment: WorkEnvironment = Field(default=WorkEnvironment.on_site)


class JobSchemaOut(JobSchemaBase):
    job_id: int
    title: str
    description: str
    salary_min: int
    salary_max: int
    job_status: JobStatus
    job_type: JobType
    work_environment: WorkEnvironment
    created_at: datetime
    updated_at: datetime


class JobUpdateSchema(JobSchemaBase):
    title: str = Field(min_length=3, max_length=100)
    description: str
    salary_min: int = Field(gt=10000)
    salary_max: int
    job_status: JobStatus
    job_type: JobType
    work_environment: WorkEnvironment
