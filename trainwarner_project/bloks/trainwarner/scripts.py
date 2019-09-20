import anyblok
from anyblok.config import Configuration
from anyblok.release import version

from logging import getLogger

from .stations import update_or_create as stations_populate


Configuration.add_application_properties(
    'populate_stations',
    [
        'logging'
    ],
    prog='Trainwarner anyblok_populate_stations, version %r' % version,
    description="""Trainwarner populate_stations script.
    This script can be used to perform a complete population of
    Model.Station table using data/stations.csv file.

    This is mainly intented for development purposes, in case of update of
    CSV parsing methods, in order to be able to run a full population with
    having to update completely database.

    [NOTE] This can be ran on production server to update Model.Station
    table."""
)


def populate_stations():

    """This is the script called by using anyblok_populate_stations -c app.dev.cfg
    This script can be used to perform a complete population of
    Model.Station table using data/stations.csv file.

    This is mainly intented for development purposes, in case of update of
    CSV parsing methods, in order to be able to run a full population with
    having to update completely database.

    [NOTE] This can be ran on production server to update Model.Station
    table."""

    registry = anyblok.start(
            'populate_stations', argparse_groups=['logging'])
    stations_populate(registry=registry)
