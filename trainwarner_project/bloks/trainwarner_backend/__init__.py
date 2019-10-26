"""Blok declaration example
"""
from anyblok.blok import Blok

from uuid import UUID
from datetime import datetime

from anyblok_pyramid.adapter import (
    uuid_adapter,
    bytes_adapter,
    datetime_adapter,
)

from pyramid.renderers import JSON

from .authorizations import update_or_create as authorizations_update_or_create


class TrainwarnerBackend(Blok):
    """Trainwarner's Blok class definition
    """

    version = "0.1.0"
    author = "Alexis Tourneux"
    required = ["anyblok-core", "auth-password", "authorization"]

    @classmethod
    def import_declaration_module(cls):
        """Python module to import in the given order at start-up
        """

        pass

    @classmethod
    def reload_declaration_module(cls, reload):
        """Python module to import while reloading server (ie when
        adding Blok at runtime
        """

        pass

    @classmethod
    def pyramid_load_config(cls, config):

        config.include("cornice")
        config.include("cornice_swagger")

        # Add renderers for JSON response format
        json_renderer = JSON()
        json_renderer.add_adapter(UUID, uuid_adapter)
        json_renderer.add_adapter(datetime, datetime_adapter)
        json_renderer.add_adapter(bytes, bytes_adapter)
        config.add_renderer("json", json_renderer)

        config.include(
            "%s.api.v1" % cls.__module__, route_prefix="/backend/api/v1"
        )

    def update(self, latest):
        """Update blok"""

        if not latest:
            self.install()
        else:
            pass

        authorizations_update_or_create(self.registry)

    def install(self):
        self.registry.User.Role.insert(
                name="common-admin", label="Common Admin Resource")
