from logging import getLogger

logger = getLogger(__name__)

_PERMISSIONS = [
    dict(
        resource="swagger", role="common-admin", perm_read=dict(matched=True)
    ),
    dict(
        resource="station-backend",
        role="common-admin",
        perm_read=dict(matched=True),
        perm_create=dict(matched=True),
        perm_update=dict(matched=True),
        perm_delete=dict(matched=False),
    ),
    dict(
        resource="user-backend",
        role="common-admin",
        perm_read=dict(matched=True),
        perm_create=dict(matched=True),
        perm_update=dict(matched=True),
        perm_delete=dict(matched=True),
    ),
    dict(
        resource="passenger-backend",
        role="common-admin",
        perm_read=dict(matched=True),
        perm_create=dict(matched=True),
        perm_update=dict(matched=True),
        perm_delete=dict(matched=True),
    ),
]


def update_or_create(registry, permissions=[]):
    """Given a list of permissions, create the permission in User.Authorization
    if it does not exists yet otherwise update it.

    :param registry: AnyBlok registry
    :param permissions: A list of permissions
    :type registry: anyblok.registry.Registry
    :type permissions: List
    :return: None
    :rtype: NoneType
    """
    if not permissions:
        permissions = _PERMISSIONS
    for item in permissions:
        if "role" in item.keys():
            item["role"] = (
                registry.User.Role.query()
                .filter_by(name=item["role"])
                .one_or_none()
            )
        if "user" in item.keys():
            item["user"] = (
                registry.User.query()
                .filter_by(login=item["user"])
                .one_or_none()
            )

        authorization = None
        if "model" in item.keys() and item.get("model"):
            authorization = (
                registry.User.Authorization.query()
                .filter_by(model=item.get("model"))
                .one_or_none()
            )
        if not authorization and (
            "resource" in item.keys() and item.get("resource")
        ):
            authorization = (
                registry.User.Authorization.query()
                .filter_by(resource=item.get("resource"))
                .one_or_none()
            )

        if authorization:
            # TODO: update only if needed
            authorization.update(**item)
        else:
            registry.User.Authorization.insert(**item)
