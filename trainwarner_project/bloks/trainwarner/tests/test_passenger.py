import pytest
from datetime import date


@pytest.mark.usefixtures("rollback_registry")
class TestPassengerModel:

    """ Test model Model.Passenger"""

    def test_insert_default(self, rollback_registry, user_1):

        """This test aims at checking that records can be properly inserted
           into Model.Passenger table."""

        registry = rollback_registry

        current_count = registry.Passenger.query().count()

        passenger_dict = dict(birthdate=date.today(), user=user_1)

        passenger = registry.Passenger.insert(**passenger_dict)

        assert registry.Passenger.query().count() == current_count + 1
        assert passenger.birthdate == passenger_dict.get("birthdate")
        assert passenger.user == user_1
