import pytest


@pytest.mark.usefixtures("rollback_registry")
class TestUser:

    """This test class is intented at tested Model.User inherited from AnyBlok
       Pyramid."""

    def test_insert_default(self, rollback_registry):

        """This test aims at checking that an user can be properly inserted.
        """

        registry = rollback_registry

        user = registry.User.insert(
            login="test_login",
            first_name="John",
            last_name="Doe",
            email="john.doe@gmail.com",
        )

        assert user.name == "John DOE"


@pytest.mark.usefixtures("rollback_registry")
class TestUserCredentials:

    """This test class is intented at tested Model.User.CredentialStore from
       AnyBlok Pyramid since Model.User was overrided."""

    def test_insert_default(self, rollback_registry, user_1):

        """This test is intented at checking that credentials can be properly
           inserted."""

        registry = rollback_registry

        credentials = registry.User.CredentialStore(
            login=user_1.login, password="test"
        )

        assert credentials.login == user_1.login
        assert credentials.password == "test"
