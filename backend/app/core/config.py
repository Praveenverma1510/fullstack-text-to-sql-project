from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NL2SQL Explorer"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 1440

    database_url: str = (
        "postgresql+psycopg2://postgres:Password%40123@localhost:5432/nl2sql_meta"
    )

    postgres_admin_url: str = (
        "postgresql+psycopg2://postgres:Password%40123@localhost:5432/postgres"
    )

    hf_model_id: str = "Qwen/Qwen2.5-1.5B-Instruct"
    hf_task: str = "text-generation"
    hf_max_new_tokens: int = 32

    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    max_upload_mb: int = 10
    enable_auth: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
