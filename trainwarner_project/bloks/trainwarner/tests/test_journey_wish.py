import pytest


@pytest.mark.usefixtures("rollback_registry")
class TestJourneyWishModel:

    """ Test model Model.JourneyWish"""

    def test_insert_default(self, rollback_registry):

        """This test aims at checking that records can be properly inserted
           into Model.JourneyWish table."""

        registry = rollback_registry

        # TODO : add user table and add an user to model
        registry.JourneyWish.insert()

    def test_get_workflow_definition(self, rollback_registry):

        """This test aims at checking the workflow defined in Model.Offer
           corresponds to chose model."""

        workflow = rollback_registry.JourneyWish.get_workflow_definition()

        expected_states = [
            "draft",
            "pending",
            "running",
            "expired",
            "cancelled",
        ]
        assert len(expected_states) == len(workflow.keys())
        for state in workflow.keys():
            assert state in expected_states
