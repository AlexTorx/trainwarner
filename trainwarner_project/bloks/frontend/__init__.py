"""Frontend Blok

Manage all public webpages

"""
import os

from anyblok.blok import Blok
from anyblok.config import Configuration


class Frontend(Blok):
    """Trainwarner's Frontend Blok class definition
    """

    version = "0.1.0"
    author = "Alexis Tourneux"
    required = ["trainwarner"]

    @classmethod
    def pyramid_load_config(cls, config):
        # Get debug_all from project configuration file
        debug = Configuration.get("pyramid.debug_all")

        # i18n
        config.add_translation_dirs(cls.__module__ + ":locale")

        # Pyramid addons
        config.include("pyramid_jinja2")

        if debug and debug is True:
            config.include("pyramid_debugtoolbar")

        # Static resources
        config.add_static_view(
            "static",
            "%s/trainwarner_project/bloks/frontend/static/" % os.getcwd(),
            cache_max_age=3600,
        )

        # Routes

        # Scan available views
        config.scan(cls.__module__ + ".views")

    def update(self, latest_version):
        """Update blok"""
        if not latest_version:
            self.install()
        else:
            pass

    #            authorizations.update_or_create(registry=self.registry)

    def install(self):
        """Create an admin user, admin role and some acl"""
        pass


#        self.registry.User.Role.insert(
#            name="consumer",
#            label="Consumer Role"
#        )
#
#        # Set user or role based authorizations on resources or models
#        authorizations.update_or_create(registry=self.registry)
