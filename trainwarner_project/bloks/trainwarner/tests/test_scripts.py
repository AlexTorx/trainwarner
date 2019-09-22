import pytest
from trainwarner_project.bloks.trainwarner.stations import (
    get_station_dict_from_row,
    update_station_file,
    update_or_create as stations_update_or_create
)

import os


@pytest.mark.usefixtures('rollback_registry')
class TestStationScript:

    """Test scripts for initializing Model.Station database table"""

    def test_get_station_dict(self):

        """This test aims at checking that function get_station_dict_from_row
           can be used properly and returns proper data representing station
        """

        input_list = [123456, 'Lille-Flandres', 'lille-flandres']

        data_dict = get_station_dict_from_row(input_list)

        assert data_dict.get('id') == 123456
        assert isinstance(data_dict.get('id'), int)
        assert data_dict.get('name') == 'Lille-Flandres'
        assert isinstance(data_dict.get('name'), str)
        assert data_dict.get('slug') == 'lille-flandres'
        assert isinstance(data_dict.get('slug'), str)

    def test_update_station_csv_file(self):

        """This test aims at checking that the function update_station_file
           is working properly."""

        # To check test validity, first extract last edition date
        here = os.path.abspath(os.path.dirname(__file__))
        last_edit = os.path.getmtime(
                os.path.join(here, '../data/stations.csv'))

        update_station_file()

        new_edit = os.path.getmtime(
                os.path.join(here, '../data/stations.csv'))

        assert new_edit > last_edit

    def test_update_or_create_stations(self, rollback_registry):

        """This test aims at checking that the update_or_create method from
           stations_script is working as intented."""

        registry = rollback_registry

        # Empty database table Model.Station in order to start test
        for station in registry.Station.query().all():
            station.delete()

        # Inject data extracted from ../data/stations.csv
        stations_update_or_create(registry=registry)

        count_after_create = registry.Station.query().count()
        assert count_after_create > 0

        # Re-inject data in order to test update
        stations_update_or_create(registry=registry)
        assert count_after_create == registry.Station.query().count()
