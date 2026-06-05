# 🚀 Job Portal API

A production-style Job Portal Backend built with FastAPI, PostgreSQL, SQLAlchemy, Alembic, JWT Authentication, and Docker.

This project allows employers to create companies and post jobs while candidates can browse jobs and submit applications.

---

## ✨ Features

### Authentication & Authorization

* User Registration
* User Login
* JWT Authentication
* Role-Based Access Control
* Candidate, Employer, and Admin Roles

### Company Management

* Create Company
* Update Company
* View Company Details
* Employer Ownership Validation

### Job Management

* Create Job Posting
* Update Job Posting
* Delete Job Posting
* View Single Job
* List Available Jobs

### Job Discovery

* Pagination
* Keyword Search
* Job Type Filtering
* Work Environment Filtering
* Salary Sorting
* Newest First Sorting

### Applications

* Apply for Jobs
* View Applications
* Track Application Status

### Database

* PostgreSQL
* SQLAlchemy ORM
* Alembic Migrations
* Seed Data Support

### Deployment

* Docker Support
* Podman Support
* Environment Variables Configuration

---

## 🛠 Tech Stack

| Technology      | Purpose               |
| --------------- | --------------------- |
| FastAPI         | API Framework         |
| PostgreSQL      | Database              |
| SQLAlchemy      | ORM                   |
| Alembic         | Database Migrations   |
| JWT             | Authentication        |
| Pydantic        | Data Validation       |
| Docker / Podman | Containerization      |
| UV              | Dependency Management |

---

## 📁 Project Structure

```text
.
├── alembic/
├── routes/
├── models.py
├── schema.py
├── db.py
├── utils.py
├── seed.py
├── main.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file:

```env
DB_URL=postgresql+psycopg://postgres:password@db:5432/job_portal
JWT_SECRET=your_secret_key
```

---

## 🚀 Local Development

### Install Dependencies

```bash
uv sync
```

### Run Migrations

```bash
uv run alembic upgrade head
```

### Seed Database

```bash
uv run python seed.py
```

### Start Server

```bash
uv run uvicorn main:app --reload
```

API will be available at:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## 🐳 Docker / Podman

### Build Containers

```bash
podman-compose build
```

### Start Services

```bash
podman-compose up -d
```

### Run Migrations

```bash
podman exec -it job_portal_api bash

uv run alembic upgrade head
```

### Seed Database

```bash
uv run python seed.py
```

---

## 📚 API Endpoints

### Authentication

| Method | Endpoint  |
| ------ | --------- |
| POST   | /register |
| POST   | /login    |

### Users

| Method | Endpoint  |
| ------ | --------- |
| GET    | /users/me |
| PATCH  | /users/me |

### Companies

| Method | Endpoint        |
| ------ | --------------- |
| POST   | /companies      |
| GET    | /companies/{id} |
| PATCH  | /companies/{id} |

### Jobs

| Method | Endpoint   |
| ------ | ---------- |
| POST   | /jobs      |
| GET    | /jobs      |
| GET    | /jobs/{id} |
| PATCH  | /jobs/{id} |
| DELETE | /jobs/{id} |

### Applications

| Method | Endpoint      |
| ------ | ------------- |
| POST   | /applications |
| GET    | /applications |

---

## 🔍 Example Job Search

```http
GET /jobs?page=1&size=10
```

### Search by Keyword

```http
GET /jobs?keyword=python
```

### Filter by Job Type

```http
GET /jobs?job_type=full_time
```

### Filter by Work Environment

```http
GET /jobs?work_environment=remote
```

### Sort by Salary

```http
GET /jobs?sort=salary_desc
```

---

## 🧪 Database Migrations

Create a Migration:

```bash
uv run alembic revision --autogenerate -m "migration name"
```

Apply Migrations:

```bash
uv run alembic upgrade head
```

Rollback One Migration:

```bash
uv run alembic downgrade -1
```

---

## 🎯 Learning Objectives

This project demonstrates:

* REST API Design
* Authentication & Authorization
* Database Modeling
* ORM Relationships
* Alembic Migrations
* Pagination
* Filtering & Sorting
* Docker Containerization
* Production-Oriented Backend Development

---

## 👨‍💻 Author

Yash

Built as a portfolio project to demonstrate backend engineering skills using FastAPI and PostgreSQL.
