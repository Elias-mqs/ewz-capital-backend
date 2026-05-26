from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
