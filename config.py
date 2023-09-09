from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "inspector"
    app_description: str = "API for Inspecting HTTP Requests"
    app_author: str = "Md Zubair Beg <inspector@zube.dev>"
    app_version: str = "0.1.0"

    # Documentation
    docs_swagger_url: str = "/docs"
    docs_redoc_url: str = "/redoc"

    # Environment
    debug: bool = False  # by default debug mode is disabled

    # Uvicorn
    uvicorn_host: str = "0.0.0.0"  # (dev/local) will be overriden by env var if set
    uvicorn_port: int = 8888  # (dev/local) will be overriden by env var if set

    # CORS
    cors_allow_origins: list[str] = ["*"]
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    # Logging
    logger_name: str = app_name
    logger_level: str = "DEBUG" if debug else "INFO"
    logger_config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s %(name)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            logger_name: {"handlers": ["default"], "level": logger_level, "propagate": False},
            "uvicorn": {"handlers": ["default"], "level": logger_level, "propagate": False},
            "": {"handlers": ["default"], "level": logger_level, "propagate": False},
        },
    }

    # read .env file, if it exists
    model_config = SettingsConfigDict(env_file=".env")
