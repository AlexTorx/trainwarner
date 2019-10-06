from anyblok import Declarations
from anyblok.column import Date, String
from anyblok.relationship import Many2One

from anyblok_postgres.column import Jsonb

register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


@register(Model)
class Passenger(Mixin.UuidColumn):

    # Find out whether birthdate should be nullable or not.
    birthdate = Date(label="Birthdate", nullable=True)

    name = String(label="Passenger Name", nullable=True)

    reduction_card = Many2One(
        label="Reduction Card",
        model=Model.ReductionCard,
        one2many="passengers",
    )

    user = Many2One(
        label="User", model=Model.User, nullable=False, one2many="passengers"
    )

    properties = Jsonb(label="properties")
