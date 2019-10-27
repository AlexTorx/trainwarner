import pytest


@pytest.mark.usefixtures("webserver")
class TestAuthLogin:

    """This test class is aimed at checking that /backend/api/v1/auth/login API
       endpoint is working as intented."""

    def test_auth_login_available_methods(self, webserver):

        """This test is aimed at checking that only POST method is available
           on API endpoint /backend/api/v1/auth/login."""

        # POST method on auth login endpoint with no parameters raises a 400
        # Bad Request HTTP response
        webserver.post_json("/backend/api/v1/auth/login", dict(), status=400)

        # All others methods will raised a 405 Method Not Available HTTP error
        response = webserver.get("/backend/api/v1/auth/login", status=405)
        assert response.status == "405 Method Not Allowed"

        response = webserver.patch(
            "/backend/api/v1/auth/login", dict(), status=405
        )
        assert response.status == "405 Method Not Allowed"

        response = webserver.put(
            "/backend/api/v1/auth/login", dict(), status=405
        )
        assert response.status == "405 Method Not Allowed"

        response = webserver.delete("/backend/api/v1/auth/login", status=405)
        assert response.status == "405 Method Not Allowed"

    def test_auth_login_success(self, webserver, admin_user):

        """This test is aimed at checking that authentication is behaving as
           intented."""

        response = webserver.post_json(
            "/backend/api/v1/auth/login",
            dict(login=admin_user.login, password="1234"),
        )

        assert response.status_code == 200
        assert "Set-Cookie" in response.headers.keys()

    def test_auth_login_fails_wrong_credentials(self, webserver, admin_user):

        """This test is aimed at checking that when wronf credentials are
           provided, authentication fails and a 401 Unauthorized HTTP error is
           raised."""

        response = webserver.post_json(
            "/backend/api/v1/auth/login",
            dict(login="not_a_valid_login", password="not_a_valid_password"),
            status=401,
        )

        assert response.status_code == 401
        assert "Set-Cookie" not in response.headers.keys()
