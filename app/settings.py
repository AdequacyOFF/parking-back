from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class SrvSettings(BaseSettings):
    app_name: str

    model_config = SettingsConfigDict(env_prefix="SRV_")


class AuthJWTSettings(BaseSettings):
    public_key: str
    private_key: str
    access_expired_at: int = 5 * 60
    refresh_expired_at: int = 7 * 24 * 60 * 60
    algorithm: str = "RS256"

    model_config = SettingsConfigDict(env_prefix="JWT_")


class AuthSettings(BaseSettings):
    otp_length: int
    otp_valid_time_minutes: int
    otp_max_attempts: int
    collector_expired_sessions_enable_cron: bool
    collector_expired_sessions_batch_size: int

    model_config = SettingsConfigDict(env_prefix="AUTH_")


class LoggingSettings(BaseSettings):
    level: str
    json_enabled: bool
    extra_context: bool
    ignore_paths: list[str]

    model_config = SettingsConfigDict(env_prefix="LOGGING_")


class DatabaseSettings(BaseSettings):
    url: str
    echo: bool

    model_config = SettingsConfigDict(env_prefix="DB_")


class RedisSettings(BaseSettings):
    host: str
    password: str

    model_config = SettingsConfigDict(env_prefix="REDIS_")


class Settings(BaseSettings):
    load_dotenv()
    srv: SrvSettings = SrvSettings()
    auth: AuthSettings = AuthSettings()
    auth_jwt: AuthJWTSettings = AuthJWTSettings()
    logging: LoggingSettings = LoggingSettings()
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()


settings = Settings()
