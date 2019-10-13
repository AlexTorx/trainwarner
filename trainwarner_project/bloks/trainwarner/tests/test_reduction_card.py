import pytest


@pytest.mark.usefixtures("rollback_registry")
class TestReductionCardModel:

    """ Test model Model.ReductionCard"""

    def test_insert_default(self, rollback_registry):

        """This test aims at checking that records can be properly inserted
           into Model.ReductionCard table."""

        registry = rollback_registry
        pass
