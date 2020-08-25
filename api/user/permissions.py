from rest_framework.permissions import BasePermission


class IsAdminOrIsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to admin (isStaff) or owner of the requested account,
        # if request.method in SAFE_METHODS:
        #     return True
        # print(obj, "||||", request.user)
        if request.user and request.user.is_staff:
            return True
        return obj == request.user
        # return True


class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to admin (isStaff) or owner of the requested account,
        # if request.method in SAFE_METHODS:
        #     return True
        # print(obj, "||||", request.user)
        # if request.user and request.user.is_staff:
        #     return True
        return obj == request.user
        # return True
