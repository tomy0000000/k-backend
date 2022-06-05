import os

from alembic import command
from alembic.config import Config
from loguru import logger
from sqlmodel import Session, create_engine

try:
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_HOST = os.environ["POSTGRES_HOST"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    POSTGRES_URI = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        "@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
except KeyError:
    logger.error("Postgres environment variables not configured.")
    raise

engine = create_engine(POSTGRES_URI, echo=True)


def alembic_upgrade():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    logger.info("Alembic upgrade completed.")


def get_session():
    with Session(engine) as session:
        yield session
