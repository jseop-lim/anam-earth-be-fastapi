from pydantic import Field, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class FileSettings(BaseSettings):
    path: FilePath = Field(validation_alias="path", default="")


class Settings(BaseSettings):
    file: FileSettings = Field(default_factory=FileSettings)

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="_")
