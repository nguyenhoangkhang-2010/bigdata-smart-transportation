from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BigData Smart Transportation Platform"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True
    
    #PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "smart_transportation"
    postgres_user: str = "bigdata"
    postgres_password: str = ""
    
    #MongoDB
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_db: str = "smart_transportation"
    
    #Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    
    #Kafka
    kafka_bootstrap_servers: str = "localhost:9092"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def postgres_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )

@lru_cache
def get_settings() -> Settings:
    return Settings()