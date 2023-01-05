from pydantic import BaseSettings, EmailStr

class Settings(BaseSettings): 
    database_hostname: str
    database_port: str
    database_password: str 
    database_name: str
    database_username: str 
    secret_key: str 
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: EmailStr

    class Config: 
        env_file = ".env"

settings = Settings() 