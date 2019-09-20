from logging import getLogger
import csv
import os


logger = getLogger(__name__)


def update_or_create(registry) -> None:

    """This method is aimed at updating or creating records in database for
       model Model.Station, from csv file."""

    logger.info("Start populating station table from CSV file.")

    here = os.path.abspath(os.path.dirname(__file__))
    path = 'data/stations.csv'

    with open(os.path.join(here, path), 'r', encoding='utf-8') as CSVfile:
        stations = csv.reader(CSVfile, delimiter=';')

        # Creating counters in order to monitor changes in database
        created = 0
        updated = 0

        # Remove CSV file headers
        next(stations)

        for station in stations:
            station_data = get_station_dict_from_row(station)

            # Find a discriminant in order to choose between update and insert
            station = registry.Station.query().filter_by(
                    id=station_data.get('id')).one_or_none()
            if station:
                station.update(**station_data)
                updated += 1
            else:
                registry.Station.insert(**station_data)
                created += 1

    logger.info(
            ("Finished populating Model.Station table.\n\tCreated stations : "
             "%d\n\tUpdated stations : %d" % (created, updated)
             )
            )


def get_station_dict_from_row(station_data) -> dict:

    """This function is supposed to return a well formatted dict for inserting
       into Model.Station table."""

    return dict(
            id=station_data[0],
            name=station_data[1],
            slug=station_data[2]
            )
