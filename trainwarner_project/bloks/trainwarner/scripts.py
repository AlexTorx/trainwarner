import anyblok
from anyblok.config import Configuration
from anyblok.release import version

from .stations import (
        update_or_create as stations_populate,
        update_station_file as stations_file_update
)
from .reduction_cards import update_or_create as reduction_cards_populate


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

Configuration.add_application_properties(
    'populate_reduction_cards',
    [
        'logging'
    ],
    prog='Trainwarner anyblok_populate_reduction_cards, version %r' % version,
    description="""Trainwarner populate_reduction_cards script.
    This script can be used to perform a complete population of
    Model.ReductionCard table.

    This is mainly intented for development purposes, in case of update of
    model Model.ReductionCard, in order to be able to run a full population
    with having to update completely database.

    [NOTE] This can be ran on production server to update Model.ReductionCard
    table."""
)

Configuration.add_application_properties(
    'update_station_file',
    [
        'logging'
    ],
    prog='Trainwarner anyblok_update_station_file, version %r' % version,
    description="""Trainwarner update_station_file script.
    This script can be used to perform a complete update of file
    data/stations.csv.

    This is mainly intented for development purposes, in case of update of
    file data/stations.csv, in order to then be able to run a full population.

    [NOTE] This can be ran on production server to update data/stations.csv
    file."""
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
    file_path = Configuration.get('stations_data')
    stations_populate(registry=registry, path=path)


def populate_reduction_cards():

    """This is the script called by using anyblok_populate_reduction_cards -c
    app.dev.cfg
    This script can be used to perform a complete population of
    Model.ReductionCard

    This is mainly intented for development purposes, in case of update of
    model Model.ReductionCard, in order to be able to run a full population
    with having to update completely database.

    [NOTE] This can be ran on production server to update Model.ReductionCard
    table."""

    registry = anyblok.start(
            'populate_reduction_cards', argparse_groups=['logging'])
    reduction_cards_populate(registry=registry)


def update_stations_file():

    """This is the script called by using anyblok_update_stations_file -c
    app.dev.cfg
    This script can be used to perform a complete update of file
    data/stations.csv.

    This is mainly intented for development purposes, in case of update of
    file data/stations.csv, in order to then be able to run a full population.

    [NOTE] This can be ran on production server to update data/stations.csv
    file."""

    stations_file_update()
