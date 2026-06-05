from db import SessionLocal
from models import (
    Application,
    Company,
    Job,
    JobApplicationStatus,
    JobStatus,
    JobType,
    User,
    UserRole,
    WorkEnvironment,
)
from utils import hash_password


def seed_users():
    users = [
        # Admin
        User(
            username="admin",
            email="admin@jobportal.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.admin,
        ),
        # Employers
        User(
            username="technova_owner",
            email="owner@technova.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.employer,
        ),
        User(
            username="startupx_owner",
            email="owner@startupx.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.employer,
        ),
        User(
            username="cloudforge_owner",
            email="owner@cloudforge.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.employer,
        ),
        # Candidates
        User(
            username="john_dev",
            email="john@example.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.candidate,
        ),
        User(
            username="alice_python",
            email="alice@example.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.candidate,
        ),
        User(
            username="bob_backend",
            email="bob@example.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.candidate,
        ),
        User(
            username="emma_sql",
            email="emma@example.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.candidate,
        ),
        User(
            username="michael_api",
            email="michael@example.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.candidate,
        ),
        User(
            username="sophia_linux",
            email="sophia@example.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.candidate,
        ),
        User(
            username="liam_django",
            email="liam@example.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.candidate,
        ),
        User(
            username="olivia_fastapi",
            email="olivia@example.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.candidate,
        ),
        User(
            username="noah_pgsql",
            email="noah@example.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.candidate,
        ),
        User(
            username="ava_cloud",
            email="ava@example.com",
            password_hash=hash_password("Password@123"),
            role=UserRole.candidate,
        ),
    ]

    with SessionLocal() as sess:
        sess.add_all(users)
        sess.commit()


def seed_companies():
    companies = [
        Company(
            name="TechNova",
            description="Backend APIs, FastAPI, Django, PostgreSQL and Cloud Solutions",
            owner_id=5,
        ),
        Company(
            name="StartupX",
            description="Artificial Intelligence, LLMs, NLP and Machine Learning Products",
            owner_id=6,
        ),
        Company(
            name="CloudForge",
            description="DevOps, Kubernetes, Docker and AWS Consulting",
            owner_id=7,
        ),
    ]
    with SessionLocal() as sess:
        sess.add_all(companies)
        sess.commit()


def seed_jobs():
    jobs = [
        # TechNova
        Job(
            title="Python Developer",
            description="Develop REST APIs using FastAPI, PostgreSQL and Docker.",
            salary_min=50000,
            salary_max=90000,
            company_id=1,
            job_status=JobStatus.opened,
            job_type=JobType.full_time,
            work_environment=WorkEnvironment.remote,
        ),
        Job(
            title="FastAPI Backend Engineer",
            description="Build scalable backend services using FastAPI and PostgreSQL.",
            salary_min=70000,
            salary_max=120000,
            company_id=1,
            job_status=JobStatus.opened,
            job_type=JobType.full_time,
            work_environment=WorkEnvironment.hybrid,
        ),
        Job(
            title="PostgreSQL Database Engineer",
            description="Design and optimize PostgreSQL databases.",
            salary_min=80000,
            salary_max=130000,
            company_id=1,
            job_status=JobStatus.opened,
            job_type=JobType.full_time,
            work_environment=WorkEnvironment.on_site,
        ),
        Job(
            title="DevOps Engineer",
            description="Manage Docker, CI/CD pipelines and cloud infrastructure.",
            salary_min=90000,
            salary_max=150000,
            company_id=1,
            job_status=JobStatus.opened,
            job_type=JobType.full_time,
            work_environment=WorkEnvironment.hybrid,
        ),
        # StartupX
        Job(
            title="AI Engineer",
            description="Build LLM and NLP applications using Python.",
            salary_min=100000,
            salary_max=180000,
            company_id=2,
            job_status=JobStatus.opened,
            job_type=JobType.full_time,
            work_environment=WorkEnvironment.remote,
        ),
        Job(
            title="Machine Learning Engineer",
            description="Train and deploy machine learning models.",
            salary_min=90000,
            salary_max=160000,
            company_id=2,
            job_status=JobStatus.opened,
            job_type=JobType.full_time,
            work_environment=WorkEnvironment.remote,
        ),
        Job(
            title="Data Engineer",
            description="Build ETL pipelines using Python and SQL.",
            salary_min=80000,
            salary_max=140000,
            company_id=2,
            job_status=JobStatus.opened,
            job_type=JobType.full_time,
            work_environment=WorkEnvironment.hybrid,
        ),
        Job(
            title="Automation Engineer",
            description="Create automation systems using Python.",
            salary_min=70000,
            salary_max=120000,
            company_id=2,
            job_status=JobStatus.opened,
            job_type=JobType.full_time,
            work_environment=WorkEnvironment.remote,
        ),
        # CloudForge
        Job(
            title="Cloud Engineer",
            description="Manage AWS infrastructure and deployments.",
            salary_min=90000,
            salary_max=160000,
            company_id=3,
            job_status=JobStatus.opened,
            job_type=JobType.full_time,
            work_environment=WorkEnvironment.hybrid,
        ),
        Job(
            title="Site Reliability Engineer",
            description="Maintain highly available distributed systems.",
            salary_min=100000,
            salary_max=170000,
            company_id=3,
            job_status=JobStatus.opened,
            job_type=JobType.full_time,
            work_environment=WorkEnvironment.on_site,
        ),
        Job(
            title="Linux System Engineer",
            description="Administer Linux servers and infrastructure.",
            salary_min=70000,
            salary_max=120000,
            company_id=3,
            job_status=JobStatus.opened,
            job_type=JobType.full_time,
            work_environment=WorkEnvironment.on_site,
        ),
        Job(
            title="Backend Developer",
            description="Develop backend APIs using Python and PostgreSQL.",
            salary_min=60000,
            salary_max=110000,
            company_id=3,
            job_status=JobStatus.opened,
            job_type=JobType.full_time,
            work_environment=WorkEnvironment.hybrid,
        ),
    ]
    with SessionLocal() as sess:
        sess.add_all(jobs)
        sess.commit()

        for job in jobs:
            sess.refresh(job)


def seed_applications():
    with SessionLocal() as sess:
        applications = [
            # Python Developer
            Application(
                job_id=25,
                user_id=8,
                resume_url="john_resume.pdf",
                status=JobApplicationStatus.submitted,
            ),
            Application(
                job_id=25,
                user_id=9,
                resume_url="alice_resume.pdf",
                status=JobApplicationStatus.reviewing,
            ),
            Application(
                job_id=25,
                user_id=10,
                resume_url="bob_resume.pdf",
                status=JobApplicationStatus.shortlisted,
            ),
            # FastAPI Backend Engineer
            Application(
                job_id=26,
                user_id=15,
                resume_url="olivia_resume.pdf",
                status=JobApplicationStatus.submitted,
            ),
            Application(
                job_id=26,
                user_id=14,
                resume_url="liam_resume.pdf",
                status=JobApplicationStatus.reviewing,
            ),
            Application(
                job_id=26,
                user_id=12,
                resume_url="michael_resume.pdf",
                status=JobApplicationStatus.shortlisted,
            ),
            # PostgreSQL Engineer
            Application(
                job_id=27,
                user_id=16,
                resume_url="noah_resume.pdf",
                status=JobApplicationStatus.reviewing,
            ),
            Application(
                job_id=27,
                user_id=13,
                resume_url="sophia_resume.pdf",
                status=JobApplicationStatus.submitted,
            ),
            # DevOps Engineer
            Application(
                job_id=28,
                user_id=13,
                resume_url="sophia_resume.pdf",
                status=JobApplicationStatus.shortlisted,
            ),
            Application(
                job_id=28,
                user_id=17,
                resume_url="ava_resume.pdf",
                status=JobApplicationStatus.submitted,
            ),
            # AI Engineer
            Application(
                job_id=29,
                user_id=17,
                resume_url="ava_resume.pdf",
                status=JobApplicationStatus.reviewing,
            ),
            Application(
                job_id=29,
                user_id=11,
                resume_url="emma_resume.pdf",
                status=JobApplicationStatus.submitted,
            ),
            Application(
                job_id=29,
                user_id=9,
                resume_url="alice_resume.pdf",
                status=JobApplicationStatus.shortlisted,
            ),
            # Machine Learning Engineer
            Application(
                job_id=30,
                user_id=11,
                resume_url="emma_resume.pdf",
                status=JobApplicationStatus.reviewing,
            ),
            Application(
                job_id=30,
                user_id=10,
                resume_url="bob_resume.pdf",
                status=JobApplicationStatus.submitted,
            ),
            # Data Engineer
            Application(
                job_id=31,
                user_id=16,
                resume_url="noah_resume.pdf",
                status=JobApplicationStatus.shortlisted,
            ),
            Application(
                job_id=31,
                user_id=8,
                resume_url="john_resume.pdf",
                status=JobApplicationStatus.reviewing,
            ),
            # Automation Engineer
            Application(
                job_id=32,
                user_id=15,
                resume_url="olivia_resume.pdf",
                status=JobApplicationStatus.submitted,
            ),
            Application(
                job_id=32,
                user_id=12,
                resume_url="michael_resume.pdf",
                status=JobApplicationStatus.rejected,
            ),
            # Cloud Engineer
            Application(
                job_id=33,
                user_id=17,
                resume_url="ava_resume.pdf",
                status=JobApplicationStatus.reviewing,
            ),
            Application(
                job_id=33,
                user_id=13,
                resume_url="sophia_resume.pdf",
                status=JobApplicationStatus.shortlisted,
            ),
            # Site Reliability Engineer
            Application(
                job_id=34,
                user_id=13,
                resume_url="sophia_resume.pdf",
                status=JobApplicationStatus.hired,
            ),
            Application(
                job_id=34,
                user_id=12,
                resume_url="michael_resume.pdf",
                status=JobApplicationStatus.reviewing,
            ),
            # Linux System Engineer
            Application(
                job_id=35,
                user_id=13,
                resume_url="sophia_resume.pdf",
                status=JobApplicationStatus.shortlisted,
            ),
            Application(
                job_id=35,
                user_id=16,
                resume_url="noah_resume.pdf",
                status=JobApplicationStatus.submitted,
            ),
            # Backend Developer
            Application(
                job_id=36,
                user_id=14,
                resume_url="liam_resume.pdf",
                status=JobApplicationStatus.reviewing,
            ),
            Application(
                job_id=36,
                user_id=15,
                resume_url="olivia_resume.pdf",
                status=JobApplicationStatus.shortlisted,
            ),
            Application(
                job_id=36,
                user_id=8,
                resume_url="john_resume.pdf",
                status=JobApplicationStatus.rejected,
            ),
        ]

        sess.add_all(applications)
        sess.commit()


if __name__ == "__main__":
    # seed_users()
    # seed_companies()
    # seed_jobs()
    seed_applications()
