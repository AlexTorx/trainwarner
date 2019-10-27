from cornice import Service

from anyblok_pyramid import current_blok

from pyramid.security import remember
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPUnauthorized


login_auth_service = Service(
    path="/auth/login",
    name="login",
    description="Login API endpoint, version 1",
    installed_blok=current_blok(),
)


@login_auth_service.post()
def login_auth_service_post(request):

    """This method is /backend/api/v1/auth/login API endpoint. It is aimed at
       authenticating users, especially on backend interfaces."""

    login = request.json_body.get("login", None)
    password = request.json_body.get("password", None)

    if not login or not password:
        raise HTTPBadRequest()

    registry = request.anyblok.registry

    credentials = dict(login=login, password=password)

    if registry.User.check_login(**credentials):
        headers = remember(request, login)
        return Response(headers=headers)

    raise HTTPUnauthorized()
