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

    # read .env file, if it exists
    model_config = SettingsConfigDict(env_file=".env")
