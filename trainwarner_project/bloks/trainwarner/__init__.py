"""Blok declaration example
"""
from anyblok.blok import Blok
from anyblok.config import Configuration
from . import stations


class Trainwarner(Blok):
    """Trainwarner's Blok class definition
    """

    version = "0.1.0"
    author = "Alexis Tourneux"
    required = [
        "anyblok-core",
        "anyblok-mixins",
        "anyblok-workflow",
        "auth-password",
        "authorization",
    ]

    @classmethod
    def import_declaration_module(cls):
        """Python module to import in the given order at start-up
        """

        from .models import user  # noqa
        from .models import reduction_card  # noqa
        from .models import passenger  # noqa
        from .models import station  # noqa
        from .models import journey_wish  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        """Python module to import while reloading server (ie when
        adding Blok at runtime
        """

        from .models import user  # noqa
        from .models import reduction_card  # noqa
        from .models import passenger  # noqa
        from .models import station  # noqa
        from .models import journey_wish  # noqa

        reload(user)
        reload(reduction_card)
        reload(passenger)
        reload(station)
        reload(journey_wish)

    @classmethod
    def pyramid_load_config(cls, config):
        pass

    def update(self, latest):
        """Update blok"""
        if not latest:
            self.install()
        else:
            stations_path = Configuration.get("stations_data")
            stations.update_or_create(
                registry=self.registry, path=stations_path
            )

    def install(self):
        stations_path = Configuration.get("stations_data")
        stations.update_or_create(registry=self.registry, path=stations_path)
        pass
