"""Blok declaration example
"""
from anyblok.blok import Blok


class Trainwarner(Blok):
    """Trainwarner's Blok class definition
    """
    version = "0.1.0"
    author = "Alexis Tourneux"
    required = ['anyblok-core', 'anyblok-mixins']

    @classmethod
    def import_declaration_module(cls):
        """Python module to import in the given order at start-up
        """
        from .models import passenger  # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        """Python module to import while reloading server (ie when
        adding Blok at runtime
        """
        from .models import passenger  # noqa
        reload(passenger)

    @classmethod
    def pyramid_load_config(cls, config):
        pass

    def update(self, latest):
        """Update blok"""
        if not latest:
            pass
