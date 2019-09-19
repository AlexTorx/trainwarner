from anyblok import Declarations
from anyblok.column import String, Date

register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


@register(Model)
class Passenger(Mixin.UuidColumn, Mixin.TrackModel):

    first_name = String(nullable=False)
    last_name = String(nullable=False)
    birthdate = Date(nullable=False)
