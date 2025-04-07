from rest_framework import permissions


class IsModeratorOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        role = getattr(request.user, 'role', None)
        role_name = getattr(role, 'name', None)
        return role_name in ["Moderator", "SuperAdmin"]


class IsModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        role = getattr(request.user, 'role', None)
        role_name = getattr(role, 'name', None)
        return role_name == "Moderator"


class SuperAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        role = getattr(request.user, 'role', None)
        role_name = getattr(role, 'name', None)
        return role_name == "SuperAdmin"


class ReadOnlyOrAuthenticatedForSpecialModels(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated


class IsOwnerOrReadOnlyForContacts(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user


class FeedbackPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        is_owner = obj.user == request.user
        role = getattr(request.user, 'role', None)
        role_name = getattr(role, 'name', None)
        is_moderator_or_admin = role_name in ["Moderator", "SuperAdmin"]

        return is_owner or is_moderator_or_admin