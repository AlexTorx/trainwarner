from anyblok_pyramid import current_blok
from anyblok_pyramid.security import AnyBlokResourceFactory

from anyblok_pyramid_rest_api.crud_resource import CrudResource, resource


@resource(
    collection_path="/users",
    path="/users/{uuid}",
    installed_blok=current_blok(),
    factory=AnyBlokResourceFactory("user-backend"),
)
class UserResource(CrudResource):

    model = "Model.User"
    resource_name = "user-backend"

    has_collection_delete = False

    has_collection_put = False
    has_collection_patch = False
