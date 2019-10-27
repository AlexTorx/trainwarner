from cornice import Service

from anyblok_pyramid import current_blok

from pyramid.security import forget
from pyramid.response import Response


logout_auth_service = Service(
    path="/auth/logout",
    name="logout",
    description="Logout API endpoint, version 1",
    installed_blok=current_blok(),
)


@logout_auth_service.get()
def logout_auth_service_get(request):

    """This method is /backend/api/v1/auth/logout API endpoint. It is aimed at
       logging out users, especially on backend interfaces."""

    # Should unauthenticated users access this API endpoint ?

    headers = forget(request)
    return Response(headers=headers)
