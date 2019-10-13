from anyblok import Declarations
from anyblok.column import Text, Selection
from anyblok_postgres.column import Jsonb

from trainwarner_project.bloks.trainwarner.reduction_cards import _CARDS

register = Declarations.register
Model = Declarations.Model
Mixin = Declarations.Mixin


@register(Model)
class ReductionCard(Mixin.UuidColumn):

    CODE = None
    NAME = None

    code = Selection(
        label="Code", selections="get_cards_codes", nullable=False
    )
    name = Text(nullable=False)
    properties = Jsonb(label="Card Properties")

    @classmethod
    def define_mapper_args(cls):
        mapper_args = super(ReductionCard, cls).define_mapper_args()
        if cls.__registry_name__ == "Model.ReductionCard":
            mapper_args.update({"polymorphic_on": cls.code})
        else:
            mapper_args.update({"polymorphic_identity": cls.CODE})
        return mapper_args

    @classmethod
    def get_cards_codes(cls):
        return {card["code"]: card["name"] for card in _CARDS}

    @classmethod
    def before_insert_orm_event(cls, connection, mapper, target):

        # Set name to current polymorphic version's name
        target.name = cls.NAME


@register(Model.ReductionCard, tablename=Model.ReductionCard)
class ChildPlus(Model.ReductionCard):

    CODE = "SNCF.CarteEnfantPlus"
    NAME = "Carte Enfant+"


@register(Model.ReductionCard, tablename=Model.ReductionCard)
class Child12v25(Model.ReductionCard):

    CODE = "SNCF.Carte1225"
    NAME = "Carte Jeune 12 - 25 ans"


@register(Model.ReductionCard, tablename=Model.ReductionCard)
class Escape(Model.ReductionCard):

    CODE = "SNCF.CarteEscapades"
    NAME = "Carte Escapades"


@register(Model.ReductionCard, tablename=Model.ReductionCard)
class Senior(Model.ReductionCard):

    CODE = "SNCF.CarteSenior"
    NAME = "Carte Senior"


@register(Model.ReductionCard, tablename=Model.ReductionCard)
class FamilyAdvantage(Model.ReductionCard):

    CODE = "SNCF.AvantageFamille"
    NAME = "Carte Avantage Famille"


@register(Model.ReductionCard, tablename=Model.ReductionCard)
class YoungAdvantage(Model.ReductionCard):

    CODE = "SNCF.AvantageJeune"
    NAME = "Carte Avantage Jeune"


@register(Model.ReductionCard, tablename=Model.ReductionCard)
class SeniorAdvantage(Model.ReductionCard):

    CODE = "SNCF.AvantageSenior"
    NAME = "Carte Enfant+"


@register(Model.ReductionCard, tablename=Model.ReductionCard)
class WeekEndAdvantage(Model.ReductionCard):

    CODE = "SNCF.AvantageWeekEnd"
    NAME = "Carte Enfant+"


@register(Model.ReductionCard, tablename=Model.ReductionCard)
class HappyCard(Model.ReductionCard):

    CODE = "SNCF.HappyCard"
    NAME = "Carte TGVmax"

    # To make requests with this card, its number (starting with 'HC') must be
    # provided
    properties = Jsonb(
        label="Card Properties", default=dict(card_number="HCxxxxxxxxx")
    )
