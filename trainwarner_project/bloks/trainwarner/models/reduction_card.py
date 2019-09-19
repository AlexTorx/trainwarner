from anyblok import Declarations
from anyblok.column import Text

register = Declarations.register
Model = Declarations.Model


@register(Model)
class ReductionCard:

    code = Text(nullable=False, primary_key=True)
    name = Text(nullable=False)
