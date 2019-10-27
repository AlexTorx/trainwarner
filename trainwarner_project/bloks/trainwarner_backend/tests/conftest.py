from anyblok.conftest import *  # noqa: F401,F403
from anyblok_pyramid.conftest import *  # noqa: F401,F403

from anyblok_pyramid.testing import init_web_server

import pytest


@pytest.fixture
def webserver(request, configuration_loaded):

    """This fixture defines a webserver that can be used in tests for making
       requests on API endpoints for instance."""

    return init_web_server()


@pytest.fixture
def fixture_webserver(request, configuration_loaded):

    """This fixture defines a webserver that is only intented to be used inside
       fixtures that require making calls to API endpoints. Indeed, webserver
       has a memory, especially for cookies and authentication tokens that may
       not be suitable for any use."""

    return init_web_server()


@pytest.fixture
def admin_user(rollback_registry):

    """This fixture provides an user with credentials with common-admin role.
    """

    user = rollback_registry.User.insert(
        email="admin@trainwarner.com",
        first_name="Alexis",
        last_name="Tourneux",
        login="admin",
    )
    rollback_registry.User.CredentialStore.insert(
        login=user.login, password="1234"
    )

    admin_role = (
        rollback_registry.User.Role.query()
        .filter_by(name="common-admin")
        .first()
    )
    admin_role.users.append(user)

    return user


@pytest.fixture
def authenticated_headers(rollback_registry, admin_user, fixture_webserver):

    """This fixture is aimed at provided authenticated headers in order to
       make requests on protected API endpoints in tests suite."""

    response = fixture_webserver.post_json(
        "/backend/api/v1/auth/login",
        dict(login=admin_user.login, password="1234"),
    )

    return {"Set-Cookie": response.headers.get("Set-Cookie")}
