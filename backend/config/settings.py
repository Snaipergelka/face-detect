from os import environ

from pydantic import BaseSettings


class DefaultSettings(BaseSettings):

    ENV: str = environ.get("ENV", "local")
    APP_HOST: str = environ.get("APP_HOST", "http://127.0.0.1")
    APP_PORT: int = int(environ.get("APP_PORT", 8080))

    DB_NAME: str = environ.get("POSTGRES_DATABASE", 'postgres')
    DB_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    DB_PORT: int = int(environ.get("POSTGRES_PORT", 5432))
    DB_USER: str = environ.get("POSTGRES_USER", "postgres")
    DB_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "postgres")
    DB_POOL_SIZE: int = int(environ.get("DB_POOL_SIZE", 15))
    DB_CONNECT_RETRY: int = int(environ.get("DB_CONNECT_RETRY", 20))

    FACE_API_KEY: str = environ.get("FACE_API_KEY")
    FACE_API_SECRET: str = environ.get("FACE_API_SECRET")
    FACE_API_URL: str = environ.get("FACE_API_URL", "https://api-us.faceplusplus.com/facepp/v3/detect"),

    MINIO_KEY: str = environ.get("MINIO_KEY")
    MINIO_SECRET: str = environ.get("MINIO_SECRET")
    MINIO_URL: str = environ.get("MINIO_URL", "http://localhost:9000")

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.DB_NAME,
            "user": self.DB_USER,
            "password": self.DB_PASSWORD,
            "host": self.DB_HOST,
            "port": self.DB_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def face_api_settings(self) -> dict:
        return {
            "api_key": self.FACE_API_KEY,
            "api_secret": self.FACE_API_SECRET,
            "url": self.FACE_API_URL
        }

    @property
    def s3_settings(self):
        return {
            "key": self.MINIO_KEY,
            "secret": self.MINIO_SECRET,
            "url": self.MINIO_URL
        }
