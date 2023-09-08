from pydantic import BaseModel


class InfoResponse(BaseModel):
    app_name: str
    app_description: str
    app_author: str
    app_version: str
