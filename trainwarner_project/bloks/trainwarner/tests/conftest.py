from anyblok.conftest import *  # noqa: F401,F403
import pytest

from datetime import date


@pytest.fixture
def paris_nord_station(rollback_registry):

    """Insert station for Paris Nord."""

    return rollback_registry.Station.insert(
        name="Paris Nord", slug="paris-nord", id=16891
    )


@pytest.fixture
def lille_flandres_station(rollback_registry):

    """Insert station for Lille-Flandres."""

    return rollback_registry.Station.insert(
        name="Lille Flandres", slug="lille-flandres", id=123
    )


@pytest.fixture
def passenger_1(rollback_registry):

    """Insert a passenger into database."""

    return rollback_registry.Passenger.insert(
        birthdate=date(year=1998, month=1, day=1)
    )
