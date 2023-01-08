import pytest
import requests

from tests.data import random_email, randon_name
from config.constants import TEST_PASSWORD


def pytest_addoption(parser):
    parser.addoption(
        "--host",
        action="store",
        default="127.0.0.1:8000",
        help="use host and port (localhost:8000) to locate your application",
    )


@pytest.fixture(scope="session")
def session():
    return requests.Session()


@pytest.fixture(scope="session")
def host(request):
    return "http://{}".format(request.config.getoption("--host"))


@pytest.fixture(scope="session")
def user(session, host):
    username = randon_name()[:16]
    user_email = random_email()

    response = session.post(
        f"{host}/signup",
        json={"email": user_email, "password": TEST_PASSWORD, "username": username},
    )

    response.raise_for_status()
    assert (
        response.json().get("username") == username
    ), f"Authorization error, wrong response: {response}"
    assert (
        response.json().get("email") == user_email
    ), f"Authorization error, wrong response: {response}"

    return response.json()


@pytest.fixture(scope="session")
def logged_in_session(session, host, user):
    response = session.post(
        f"{host}/token",
        data={"username": user.get("username"), "password": TEST_PASSWORD},
    )
    response.raise_for_status()
    session.headers["Authorization"] = f"Bearer {response.json().get('access_token')}"
    return session
