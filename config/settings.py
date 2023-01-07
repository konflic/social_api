import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_PORT: str = os.getenv("DB_PORT")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_USER: str = os.getenv("DB_USER")
    DB_HOST: str = os.getenv("DB_HOST")
    secret_key: str = os.getenv("SECRET")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire: int = 600  # seconds


settings = Settings()
