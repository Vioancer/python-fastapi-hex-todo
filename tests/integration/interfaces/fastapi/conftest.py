import pytest
from fastapi.testclient import TestClient  # type: ignore

from tests.utils.database import clear_database
from todolist.config.environment import get_current_settings, get_initial_settings
from todolist.interfaces.fastapi.app import init_app


# Settings fixtures
@pytest.fixture(name="current_env_settings")
def current_env_settings_fixture():
    return get_current_settings()


@pytest.fixture(name="initial_env_settings")
def initial_env_settings_fixture():
    return get_initial_settings()


# Web app fixtures
@pytest.fixture(name="web_app_factory")
def web_app_factory_fixture():
    return lambda settings: init_app(settings)


@pytest.fixture(name="web_app")
def web_app_fixture(web_app_factory, current_env_settings):
    return web_app_factory(current_env_settings)


# Test client fixtures
@pytest.fixture(name="test_client_factory")
def test_client_factory_fixture():
    return lambda app: TestClient(app)


@pytest.fixture(name="test_client")
def test_client_fixture(web_app, test_client_factory):
    clear_database()
    return test_client_factory(web_app)
