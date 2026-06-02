from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_URL: str | None = getenv("DB_URL")
if DB_URL is None:
    raise ValueError("Database url could not load!")


engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_conn():
    sess = SessionLocal()
    try:
        yield sess
    finally:
        sess.close()
