from logging import getLogger

logger = getLogger(__name__)

_CARDS = [
        dict(
            code="SNCF.CarteEnfantPlus",
            name="Carte Enfant+"
        ),
        dict(
            code="SNCF.Carte1225",
            name="Carte Jeune 12 - 25 ans"
        ),
        dict(
            code="SNCF.CarteEscapades",
            name="Carte Escapades"
        ),
        dict(
            code="SNCF.CarteSenior",
            name="Carte Senior"
        ),
        dict(
            code="SNCF.AvantageFamille",
            name="Carte Avantage Famille"
        ),
        dict(
            code="SNCF.AvantageJeune",
            name="Carte Avantage Jeune"
        ),
        dict(
            code="SNCF.AvantageSenior",
            name="Carte Avantage Senior"
        ),
        dict(
            code="SNCF.AvantageWeekEnd",
            name="Carte Avantage Week-End"
        ),
        dict(
            code="SNCF.HappyCard",
            name="Carte TGVMax"
        )
    ]

def update_or_create(registry, cards=[]):

    """This function aims at initializing reduction cards when installing or
       updating trainwarner blok."""

    logger.info("Starting to import reduction cards.")

    if not cards:
        cards = _CARDS

    for card in cards:
        exists = registry.ReductionCard.query().filter_by(
                code=card.get('code')).one_or_none()

        if not exists:
            registry.ReductionCard.insert(**card)
        else:
            exists.update(**card)

    logger.info("Reduction cards succesfully imported.")
