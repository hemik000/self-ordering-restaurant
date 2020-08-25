from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound


class IsSessionActive(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        # if request.method in SAFE_METHODS:
        #     return True
        if request.customer is not None:
            return True

        raise NotFound({"message": "Customer token not found"})

        # return True
