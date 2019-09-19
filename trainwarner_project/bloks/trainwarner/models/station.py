from anyblok import Declarations
from anyblok.column import Text, Integer

register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


@register(Model)
class Station():

    """This model has Model.Station as a namespace. It is intented for storing
       known stations extracted from a stations.csv file."""

    id = Integer(primary_key=True)
    name = Text(nullable=False)
    slug = Text(nullable=False)
