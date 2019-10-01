import pytest


@pytest.mark.usefixtures("rollback_registry")
class TestStationModel:

    """ Test model Model.Station"""

    def test_insert_default(self, rollback_registry):

        """This test aims at checking that records can be properly inserted
           into Model.Station table."""

        registry = rollback_registry

        current_count = registry.Station.query().count()

        # Assuming that Model.Station table is already filled with data, set
        # unused id
        station_dict = dict(
            id=100000, name="station name", slug="station-slug"
        )

        station = registry.Station.insert(**station_dict)

        assert registry.Station.query().count() == current_count + 1
        assert station.id == station_dict.get("id")
        assert station.name == station_dict.get("name")
        assert station.slug == station_dict.get("slug")
