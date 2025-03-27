from typing import Literal, Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="tap_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    environment: Literal["production", "development"] = "development"

    logging_dict: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            },
        },
        "handlers": {
            "stdout": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["stdout"],
                "level": "WARNING",
                "propagate": False,
            },
            "apolonia": {
                "handlers": ["stdout"],
                "level": "INFO",
                "propagate": False,
            },
            "__main__": {  # if __name__ == '__main__'
                "handlers": ["stdout"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    title: str = "Vinted Automation API"
    db_url: str