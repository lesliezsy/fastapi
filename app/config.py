from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    # when an instance of Settings is created, it will automatically read environment variables from the .env file and populate the attributes of the Settings class accordingly. This is a feature provided by Pydantic's BaseSettings to simplify configuration management.
    class Config:
        env_file = ".env"

settings = Settings()

