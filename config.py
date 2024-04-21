from dotenv import load_dotenv
import os


class Settings:
    POSTGRES_DATABASE_URLS: str = "postgresql://postgres:postgres@localhost:5432/db"
    POSTGRES_DATABASE_URLA: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/db"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str


load_dotenv()
settings = Settings()

#settings.POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
settings.POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT', 5432))
settings.POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
settings.POSTGRES_USER = os.environ.get('POSTGRES_USER')
settings.POSTGRES_DB = os.environ.get('POSTGRES_DB')
settings.POSTGRES_HOST = os.environ.get('POSTGRES_HOST')

settings.POSTGRES_DATABASE_URLS = f"postgresql:" \
                                  f"//{settings.POSTGRES_USER}:" \
                                  f"{settings.POSTGRES_PASSWORD}" \
                                  f"@{settings.POSTGRES_HOST}:" \
                                  f"{settings.POSTGRES_PORT}" \
                                  f"/{settings.POSTGRES_DB}"

settings.POSTGRES_DATABASE_URLA = f"postgresql+asyncpg:" \
                                  f"//{settings.POSTGRES_USER}:" \
                                  f"{settings.POSTGRES_PASSWORD}" \
                                  f"@{settings.POSTGRES_HOST}:" \
                                  f"{settings.POSTGRES_PORT}" \
                                  f"/{settings.POSTGRES_DB}"



