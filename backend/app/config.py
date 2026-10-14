from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_test_db: str
    postgres_host: str
    postgres_port: int

    def _build_url(self, database: str) -> URL:
        return URL.create(
            "postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=database,
        )

    @property
    def database_url(self) -> URL:
        return self._build_url(self.postgres_db)

    @property
    def test_database_url(self) -> URL:
        return self._build_url(self.postgres_test_db)


settings = Settings()
