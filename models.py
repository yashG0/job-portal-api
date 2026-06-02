from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserRole(str, Enum):
    candidate = "Candidate"
    employer = "Employer"
    admin = "Admin"


class JobStatus(str, Enum):
    hold = "Hold"
    closed = "Closed"
    opened = "Open"


class JobType(str, Enum):
    full_time = "Full Time"
    part_time = "Part Time"
    internship = "Internship"
    contract = "Contract"
    freelance = "Freelance"


class WorkEnvironment(str, Enum):
    on_site = "On Site"
    remote = "Remote"
    hybrid = "Hybrid"


class JobApplicationStatus(str, Enum):
    submitted = "Submitted"
    reviewing = "Reviewing"
    shortlisted = "Shortlisted"
    hired = "Hired"
    rejected = "Rejected"


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(default=UserRole.candidate)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    companies: Mapped[list["Company"]] = relationship(back_populates="owner")
    applications: Mapped[list["Application"]] = relationship(back_populates="user")


class Company(Base):
    __tablename__ = "companies"

    company_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    owner: Mapped["User"] = relationship(back_populates="companies")
    jobs: Mapped[list["Job"]] = relationship(back_populates="company")


class Job(Base):
    __tablename__ = "jobs"

    job_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    salary_min: Mapped[int] = mapped_column()
    salary_max: Mapped[int] = mapped_column()
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.company_id"))
    job_status: Mapped[JobStatus] = mapped_column(default=JobStatus.opened)
    job_type: Mapped[JobType] = mapped_column()
    work_environment: Mapped[WorkEnvironment] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    company: Mapped["Company"] = relationship(back_populates="jobs")
    applications: Mapped[list["Application"]] = relationship(back_populates="job")


class Application(Base):
    __tablename__ = "applications"

    application_id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.job_id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    resume_url: Mapped[str] = mapped_column(String(500))
    status: Mapped[JobApplicationStatus] = mapped_column(
        default=JobApplicationStatus.submitted
    )

    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
    job: Mapped["Job"] = relationship(back_populates="applications")
    user: Mapped["User"] = relationship(back_populates="applications")
