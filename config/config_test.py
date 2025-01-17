import os
from typing import Generator

import pytest
from pydantic import BaseModel

from config.config import BaseConfig


class ServerConfig(BaseModel):
    host: str
    port: int


class AppConfig(BaseConfig):
    name: str
    server: ServerConfig


@pytest.fixture
def set_env() -> Generator[None, None, None]:
    os.environ["APP_ENV"] = "test"
    os.environ["APP_CONFIG_PATH"] = "testdata/"

    yield

    del os.environ["APP_ENV"]
    del os.environ["APP_CONFIG_PATH"]


def test_get_cfg_yaml_file(set_env: None):
    load_config = AppConfig.load()
    expected_config = AppConfig(
        cfg_folder="testdata/",
        app_env="test",
        default_file_name="default",
        name="myapp",
        server=ServerConfig(
            host="testhost",
            port=8001,
        ),
    )
    assert load_config == expected_config

    os.environ["APP_ENV"] = "test2"
    load2 = AppConfig.load()
    expected_config.server.host = "test2host"
    assert load2 == expected_config
