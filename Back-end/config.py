from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "change_this_to_a_real_secret"   # production me env var se load karo
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

settings = Settings()