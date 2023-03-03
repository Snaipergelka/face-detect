import os
from backend.config.settings import DefaultSettings


def get_settings() -> DefaultSettings:
    env = os.environ.get("ENV", "local")
    if env == "local":
        return DefaultSettings()

    return DefaultSettings()  # fallback to default
