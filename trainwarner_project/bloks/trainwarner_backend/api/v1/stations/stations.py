from anyblok_pyramid import current_blok
from anyblok_pyramid.security import AnyBlokResourceFactory

from anyblok_pyramid_rest_api.crud_resource import CrudResource, resource


@resource(
    collection_path="/stations",
    path="/stations/{uuid}",
    installed_blok=current_blok(),
    factory=AnyBlokResourceFactory("station-backend"),
)
class StationResource(CrudResource):

    model = "Model.Station"
    resource_name = "station-backend"

    has_delete = False
    has_collection_delete = False

    has_collection_post = False

    has_collection_put = False
    has_collection_patch = False
