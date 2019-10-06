import pytest
from datetime import date, datetime, timedelta


@pytest.mark.usefixtures("rollback_registry")
class TestJourneyWishModel:

    """ Test model Model.JourneyWish"""

    def test_insert_default(self, rollback_registry, user_1):

        """This test aims at checking that records can be properly inserted
           into Model.JourneyWish table."""

        registry = rollback_registry

        # TODO : add user table and add an user to model
        registry.JourneyWish.insert(user=user_1)

    def test_insert_journey_wish(
        self,
        rollback_registry,
        lille_flandres_station,
        paris_nord_station,
        passenger_1,
        user_1,
    ):

        """This test is intented at checking that data can be inserted into
           a Model.JourneyWish database record."""

        registry = rollback_registry

        journey_wish = registry.JourneyWish.insert(
            departure=lille_flandres_station,
            arrival=paris_nord_station,
            from_date=datetime(year=2019, month=10, day=5, hour=12, minute=30),
            end_date=datetime(year=2019, month=10, day=5, hour=14),
            activation_date=date.today(),
            user=user_1,
        )

        journey_wish.passengers.append(passenger_1)

        assert journey_wish.departure == lille_flandres_station
        assert journey_wish.arrival == paris_nord_station
        assert journey_wish.from_date.replace(tzinfo=None) == datetime(
            year=2019, month=10, day=5, hour=12, minute=30
        )
        assert journey_wish.end_date.replace(tzinfo=None) == datetime(
            year=2019, month=10, day=5, hour=14
        )
        assert journey_wish.activation_date == date.today()

        assert journey_wish.passengers == [passenger_1]
        assert journey_wish.user == user_1

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

    def test_activate_journey_wish(self, rollback_registry, user_1):

        """This test is aimed at checking that the activate function is working
           as intented."""

        registry = rollback_registry

        journey_wish = registry.JourneyWish.insert(user=user_1)

        assert journey_wish.state == "draft"
        assert not journey_wish.active
        assert not journey_wish.activation_date

        journey_wish.activate("draft")
        assert journey_wish.state == "draft"
        assert journey_wish.active
        assert journey_wish.activation_date == date.today()

    def test_deactivate_journey_wish(self, rollback_registry, user_1):

        """This test is aimed at checking that the deactivate function is
           working as intented."""

        registry = rollback_registry

        journey_wish = registry.JourneyWish.insert(user=user_1)

        # By default journey_wish is not activated so start by activating it
        # before deactivating it
        journey_wish.activate("draft")

        journey_wish.deactivate("draft")
        assert journey_wish.state == "draft"
        assert not journey_wish.active

    def test_journey_wish_check_state(self, rollback_registry, user_1):

        """This test is aimed at checking that the check_state method from
           Model.JourneyWish is working as intented in the different possible
           cases."""

        registry = rollback_registry

        journey_wish = registry.JourneyWish.insert(user=user_1)

        # First, check state with init state at "draft"
        journey_wish.check_state()

        assert journey_wish.state == "draft"
        assert not journey_wish.active

        # Next, go to "pending" state and check state
        journey_wish.state_to("pending")
        journey_wish.check_state()

        # Check that state has not change since no more data were provided
        assert journey_wish.state == "pending"
        assert not journey_wish.active

        journey_wish.activation_date = date.today() - timedelta(days=1)
        journey_wish.check_state()

        assert journey_wish.state == "running"
        assert journey_wish.active

        # Next set from_date in the past to make it expire
        journey_wish.from_date = datetime.now() - timedelta(hours=1)
        journey_wish.check_state()

        assert journey_wish.state == "expired"
        assert not journey_wish.active
