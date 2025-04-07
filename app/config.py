from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expires_minutes: int
    cloud_name: str
    cloud_api_key: int
    cloud_api_secret: str

    class Config:
        env_file = ".env"


settings = Settings()
