from anyblok.conftest import *  # noqa: F401,F403
import pytest


@pytest.fixture
def paris_nord_station(self, rollback_registry):

    """Insert station for Paris Nord."""

    return rollback_registry.Station.insert(
        name="Paris Nord",
        slug="paris-nord",
        id=16891)


@pytest.fixture
def lille_flandres_station(self, rollback_registry):

    """Insert station for Lille-Flandres."""

    return rollback_registry.Station.insert(
        name="Lille Flandres",
        slug="lille-flandres",
        id=123)
