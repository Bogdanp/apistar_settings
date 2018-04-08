import pytest

from apistar import App, Route, TestClient, validators
from apistar_settings import Settings, SettingsComponent


def index(settings: Settings) -> dict:
    return settings


routes = [
    Route("/", method="GET", handler=index),
]

components = [
    SettingsComponent({
        "APP_NAME": validators.String(),
        "WORKERS": validators.Integer(default=10),
    }),
]


@pytest.fixture(scope="session")
def app():
    return App(routes=routes, components=components)


@pytest.fixture
def client(app):
    return TestClient(app)


def test_settings_component_can_inject_settings(client):
    # Given that I have envirnoment variables for all my settings
    # When I call the index endpoint
    response = client.get("/")

    # Then I should get back my settings
    assert response.json() == {
        "APP_NAME": "example",
        "WORKERS": 2,
    }
