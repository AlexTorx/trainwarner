import pytest
from datetime import date


@pytest.mark.usefixtures('rollback_registry')
class TestJourneyWishModel:

    """ Test model Model.JourneyWish"""

    def test_insert_default(self, rollback_registry):

        """This test aims at checking that records can be properly inserted
           into Model.JourneyWish table."""

        registry = rollback_registry
        pass