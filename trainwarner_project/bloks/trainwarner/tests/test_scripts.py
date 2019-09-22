import pytest
from trainwarner_project.bloks.trainwarner.stations import (
    get_station_dict
)


@pytest.mark.usefixtures('rollback_registry')
class TestStationScript:

    """ Test scripts for initializing database tables"""

    def test_get_station_dict(self):

        """This test aims at checking that function get_station_dict can be
           used properly and returns proper data representing station"""

        input_list = [123456, 'Lille-Flandres', 'lille-flandres']

        data_dict = get_station_dict(input_list)

        assert data_dict.get('id') == 123456
        assert data_dict.get('name') == 'Lille-Flandres'
        assert data_dict.get('slug') == 'lille-flandres'