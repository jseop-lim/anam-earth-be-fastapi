from pydantic import Field, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class FilePathSettings(BaseSettings):
    node: FilePath = Field(validation_alias="node")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    file_path: FilePathSettings = Field(
        default_factory=FilePathSettings,  # type: ignore
    )
