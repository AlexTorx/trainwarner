import pytest


@pytest.mark.usefixtures('rollback_registry')
class TestReductionCardModel:

    """ Test model Model.ReductionCard"""

    def test_insert_default(self, rollback_registry):

        """This test aims at checking that records can be properly inserted
           into Model.ReductionCard table."""

        registry = rollback_registry

        current_count = registry.ReductionCard.query().count()

        card_dict = dict(
            name='My test reduction Card',
            code='test.Card'
        )

        card = registry.ReductionCard.insert(**card_dict)

        assert registry.ReductionCard.query().count() == current_count + 1
        assert card.name == card_dict.get('name')
        assert card.code == card_dict.get('code')