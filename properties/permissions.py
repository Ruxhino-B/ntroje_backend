from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPropertyOwnerOrReadOnly(BasePermission):
    """
    Read-only access for everyone.
    Write access only for the owner of the property.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user