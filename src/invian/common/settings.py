from pydantic import AnyUrl, BaseSettings, Field, MongoDsn, RedisDsn


class _Settings(BaseSettings):
    INTERVAL: int = Field(default=5)
    REDIS_URL: RedisDsn = Field(default="redis://localhost:6379")
    MONGODB_URL: MongoDsn = Field(default="mongodb://invian:invian@localhost:27017")
    CONTROLLER_TCP_URL: AnyUrl = Field(default="tcp://localhost:1111")
    CONTROLLER_API_URL: AnyUrl = Field(default="http://localhost:8000")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_prefix = "INVIAN_"


settings = _Settings()
