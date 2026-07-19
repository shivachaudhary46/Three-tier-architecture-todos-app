from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str 
    SECRET_KEY: str
    ALGO: str = "HS256"
    ACCESS_TOKEN_EXPIRE: int = 30 # minutes
    ENVIRONMENT: str = "developement"

    model_config = {
        "extra": "allow",
        "env_file": ".env"
    }

settings = Settings() 
