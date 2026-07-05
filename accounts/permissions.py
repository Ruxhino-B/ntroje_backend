from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAgent(BasePermission):
    """Only agents can access."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'agent')


class IsManager(BasePermission):
    """Managers and admins can access."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in ('manager', 'admin'))


class IsOwner(BasePermission):
    """Only owners can access."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'owner')


class IsAdminRole(BasePermission):
    """Only admin-role users (not just is_staff)."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')


class IsAgentOrManager(BasePermission):
    """Agents, managers, owners and admins — anyone who manages listings."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in ('agent', 'manager', 'owner', 'admin'))


class IsAgentOrManagerOrReadOnly(BasePermission):
    """
    Read-only for everyone (including anonymous).
    Write access only for agents / managers / owners / admins.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in ('agent', 'manager', 'owner', 'admin'))


class IsObjectOwner(BasePermission):
    """
    Object-level: user can only modify their own object.
    The model must expose a `user` FK or `owner` FK.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        owner = getattr(obj, 'user', None) or getattr(obj, 'owner', None)
        return owner == request.user
