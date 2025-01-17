import logging
import os
from typing import Any, Self

from pydantic_settings import (
    BaseSettings,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)

logger = logging.getLogger(__name__)


class BaseConfig(BaseSettings):
    cfg_folder: str = ""
    app_env: str = ""
    default_file_name: str = ""

    @classmethod
    def load(
        cls,
        cfg_folder: str = "config/",
        app_env: str = "local",
        default_file_name: str = "default",
        **kwargs: Any,
    ) -> Self:
        cfg_folder = os.environ.get("APP_CONFIG_PATH", cfg_folder)
        app_env = os.environ.get("APP_ENV", app_env)
        logger.info(f"Loading config from {cfg_folder} for {app_env}")

        return cls(
            cfg_folder=cfg_folder,
            app_env=app_env,
            default_file_name=default_file_name,
            **kwargs,
        )

    @classmethod
    def get_cfg_yaml_file(
        cls,
        file_prefix: str = "default",
        cfg_folder: str = "config/",
    ):
        """
        Return the path to the configuration YAML file.

        Returns the path to the configuration YAML file, as specified by the
        APP_CONFIG_PATH environment variable. If the variable is not set, the
        default value is "config/".

        :return: The path to the configuration YAML file.
        :rtype: str
        """
        file_name = file_prefix + ".yaml"
        return os.path.join(os.getcwd(), cfg_folder, file_name)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        init_args = init_settings()
        cfg_folder = init_args["cfg_folder"]
        app_env = init_args["app_env"]
        default_file_name = init_args["default_file_name"]
        app_file = cls.get_cfg_yaml_file(file_prefix=app_env, cfg_folder=cfg_folder)
        default_file = cls.get_cfg_yaml_file(
            file_prefix=default_file_name, cfg_folder=cfg_folder
        )
        return (
            EnvSettingsSource(
                settings_cls,
                env_prefix="APP_",
                env_nested_delimiter="__",
                case_sensitive=False,
            ),
            YamlConfigSettingsSource(settings_cls, yaml_file=app_file),
            YamlConfigSettingsSource(settings_cls, yaml_file=default_file),
        )
